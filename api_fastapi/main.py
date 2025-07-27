import os, logging, httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api_fastapi.routeurs import (
    routeur_bdd, routeur_etl, routeur_s3, routeur_elk
)

from api_utils.commons import get_env_variable

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def lifespan(_):
    print(f"➡️ Startup server".center(os.get_terminal_size().columns))
    yield
    print("❌ Shutdown server".center(os.get_terminal_size().columns))

app = FastAPI(
    title = get_env_variable("APP_NAME", compulsory=True),
    description = get_env_variable("APP_DESCRIPTION"),
    version = get_env_variable("APP_VERSION", compulsory=True), # lire depuis le fichier VERSION a la racine
    # lifespan = lifespan,
    docs_url = "/docs", # /docs
)

origins, methods, headers = ["*"], ["*"], ["*"] 
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = methods,
    allow_headers = headers
)

@app.get("/", tags=["ping 🙋‍♂️"])
async def start():
    logging.info("Server started !")
    return {
        "message": "Ping hello from server !",
        "app-name": get_env_variable("APP_NAME"),
        "version": get_env_variable("APP_VERSION"),
        "env": get_env_variable("ENV")
    }

@app.get("/health", tags=["health check"])
async def health_check():
    """
    Health check endpoint to verify if the server is running.
    """
    return {"status": "ok", "message": "Server is running!"}


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

app.include_router(routeur_bdd.router)
app.include_router(routeur_etl.router)
app.include_router(routeur_s3.router)
app.include_router(routeur_elk.router)