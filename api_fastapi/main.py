import os
import yappi
import httpx
import logging
import asyncio
import threading
from fastapi import FastAPI, Request, Response
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from prefect.workers.process import ProcessWorker

from prometheus_client import (
    start_http_server, Gauge, generate_latest, CONTENT_TYPE_LATEST, REGISTRY
)

from api_fastapi.routeurs import (
    routeur_bdd, routeur_etl, routeur_services
)

from api_utils.commons import get_env_variable

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


API_NAME = get_env_variable("API_NAME", default_value="DPE-ENEDIS-ADEME-API-SERVER", compulsory=True)
API_DESCR = get_env_variable("API_DESCRIPTION", default_value="API backend for DPE Energy Performance Analysis")
API_VERSION = get_env_variable("API_VERSION", default_value="1.0.0", compulsory=True) # TODO lire depuis le fichier VERSION a la racine

logger = logging.getLogger(API_NAME)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s - %(name)s - %(message)s")

# prometheus gauges
# CPU gauge
yappi_gauge = Gauge(
    "yappi_function_cpu_seconds",
    "CPU time per Python function",
    ["module", "function"]
)
# Gauge for function call count
yappi_ncalls = Gauge(
    "yappi_function_ncalls",
    "Number of calls per Python function",
    ["module", "function"]
)

# ceci permet de démarrer un agent prefect dans le conteneur pour exécuter les déploiements
worker_thread: threading.Thread | None = None

def run_worker():
    """Fonction pour lancer le worker dans un thread séparé."""
    async def main():
        worker = ProcessWorker(work_pool_name="dpe-api-prefect-agent")
        await worker.start()
    asyncio.run(main())

@asynccontextmanager
async def lifespan(app: FastAPI):
    # global worker
    #worker = ProcessWorker(work_pool_name="dpe-api-prefect-agent")
    #await worker.start()
    global worker_thread
    # Démarrer le thread du worker
    worker_thread = threading.Thread(target=run_worker, daemon=True)
    worker_thread.start()
    logger.info("✅ Prefect worker started")
    try: 
        yield
    finally:
        print("shut down worker agent")


app = FastAPI(
    title = API_NAME,
    description = API_DESCR,
    version = API_VERSION,
    docs_url = "/docs",
    lifespan=lifespan
)

origins, methods, headers = ["*"], ["*"], ["*"] 
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = methods,
    allow_headers = headers
)

limiter = Limiter( # rate limiter instance
    key_func=get_remote_address, 
    storage_uri=f"redis://{os.getenv("REDIS_HOST"):{os.getenv("REDIS_PORT")}}"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/", tags=["🙋‍♂️ health check"])
async def start():
    logger.info("Server started !")
    return {
        "message": "Ping hello from server !",
        "app-name": get_env_variable("APP_NAME"),
        "version": get_env_variable("APP_VERSION"),
        "env": get_env_variable("ENV")
    }

@app.get("/health", tags=["🙋‍♂️ health check"])
async def health_check():
    """Health check endpoint to verify if the server is running."""
    return {"status": "ok", "message": "Server is running!"}


@app.get("/profiling", tags=["🙋‍♂️ health check"])
async def get_profile():
    from pathlib import Path
    # Current project folder
    project_root = Path(__file__).parent.parent.resolve()
    # logger.info(f"yappi will show profiling related to : {project_root}")
    yappi.stop()
    stats = yappi.get_func_stats()
    # Filter functions whose source files are inside the project folder
    filtered_stats = [
        func for func in stats
        if func.full_name and Path(func.full_name).resolve().is_relative_to(project_root)
        and ("Library" not in Path(func.full_name).parts) 
        and (".venv" not in Path(func.full_name).parts)
        and ("<" not in func.module)
        and ("<" not in func.name)
    ]
    # read stats 
    # result = []
    # for func in filtered_stats:
    #     result.append({
    #         "name": func.name,
    #         "module": func.module,
    #         "ncall": func.ncall,
    #         "ttot": func.ttot,  # total time
    #         "tsub": func.tsub   # time spent in subfunctions
    #     })
    # return result

    # update prometheus metrics
    logger.info(f"Collected ({len(filtered_stats)}) metrics")
    for func in filtered_stats:
        yappi_gauge.labels(module=func.module, function=func.name).set(func.ttot)
        yappi_ncalls.labels(module=func.module, function=func.name).set(func.ncall)
    yappi.clear_stats()
    yappi.start(builtins=False, profile_threads=True)  # restart for next collection
    return Response(generate_latest(REGISTRY), 200, media_type=CONTENT_TYPE_LATEST)


@app.get("/price_kwh", tags=["price"])
async def get_kwh_price():
    """
    Endpoint to get the price of kWh in euros.
    This call another public api to get the current price.
    """
    URL_PRICING_KWH, prix_bckp = "https://open-dpe.fr/api/v1/electricity.php?tarif=EDF_bleu", 0.200
    metadata_tarif = {
        'source': URL_PRICING_KWH,
        'description': 'Tarif EDF reglementé - fixé par les pouvoirs publics.',
        'url': 'https://particulier.edf.fr/fr/accueil/electricite-gaz/tarif-bleu.html',
        'date_tarif': '01/02/2025',
        'date_extraction': '09/02/2025',
        'prix_kwh_base': prix_bckp, # prix backp
        'prix_hc': 'NC',
        'prix_hp': 'NC'
    }
    try:
        query_pricing = httpx.get(URL_PRICING_KWH, timeout=30) # 30s timeout
        query_pricing.raise_for_status()  # raise an error for bad responses
        res = query_pricing.json()
        metadata_tarif.update({
            'date_tarif': res.get('date_tarif', 'NA'),
            'date_extraction': res.get('date_extraction', 'NA'),
            'prix_kwh_base': res.get('options', {}).get('base', {}).get('prix_kWh', prix_bckp),
        })
    except httpx.TimeoutException:
        print("Timeout occurred while fetching pricing data.")
    except Exception as e:
        print(f"Error occurred while fetching pricing data: {e}")
    finally:
        return metadata_tarif

@app.get("/adresses-strict", tags=['database'])
@limiter.limit("5/minute") 
async def limited_endpoint(request: Request):
    """up to 5 requests per minute per IP"""
    return {"message": "You can call this endpoint up to 5 times per minute."}

app.include_router(routeur_bdd.auth_router)
app.include_router(routeur_bdd.router)
app.include_router(routeur_etl.router)
app.include_router(routeur_services.router)