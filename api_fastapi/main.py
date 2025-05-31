import os, logging, httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api_fastapi.routeurs import routeur_bdd, routeur_etl, routeur_s3


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = FastAPI(
    title = os.getenv("app-name", ""),
    description = os.getenv("app-description"),
    version = os.getenv("app-version") # lire depuis le fichier VERSION a la racine
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
def start():
    logging.INFO("Server started !")
    return {
        "message": "Ping hello from server !",
        "app-name": os.getenv("app-name"),
        "version": os.getenv("app-version"),
        "env": os.getenv("ENV")
    }

@app.get("/health", tags=["health check"])
def health_check():
    """
    Health check endpoint to verify if the server is running.
    """
    return {"status": "ok", "message": "Server is running!"}


@app.get("/price_kwh", tags=["price"])
def get_kwh_price():
    """
    Endpoint to get the price of kWh in euros.
    This call another public api to get the current price.
    """

    URL_PRICING_KWH, prix_bckp = "https://open-dpe.fr/api/v1/electricity.php?tarif=EDF_bleu", 0.216

    metadata_tarif = {
        'source': URL_PRICING_KWH,
        'description': 'Tarif reglementé - fixé par les pouvoirs publics.',
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