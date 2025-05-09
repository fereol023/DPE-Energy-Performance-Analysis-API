import os, logging
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

app.get("/", tags=["ping 🙋‍♂️"])
def start():
    logging.INFO("Server started !")
    return {
        "message": "Ping hello from server !",
        "app-name": os.getenv("app-name"),
        "version": os.getenv("app-version"),
        "env": os.getenv("ENV")
    }

app.include_router(routeur_bdd.router)
app.include_router(routeur_etl.router)
app.include_router(routeur_s3.router)