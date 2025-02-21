from fastapi import FastAPI
from pymongo import MongoClient
import os

app = FastAPI()

_config = {
    "ENVIRONMENT": os.getenv("ENVIRONMENT", "PROD"),
    "DB_HOST": os.getenv("DB_HOST", None),
    "DB_PORT": int(os.getenv("DB_PORT", 27017)),
    "DB_USER": os.getenv("DB_USER", None),
    "DB_PWD": os.getenv("DB_PWD", None),
    "DB_NAME": os.getenv("DB_NAME", "dpe_database")
}


def load_db(config):
    try:
        client = MongoClient(
            host=config.get('DB_HOST'), 
            port=config.get('DB_PORT'), 
            # username=config.get('DB_USER'), 
            # password=config.get('DB_PWD'),
            # authSource="admin"  # a retirer
            )
        db = client[config.get("DB_NAME")]
        return db
    except Exception as e:
        print(f"Error while loading db : {e}")

get_collection = lambda db, collection_name: db[collection_name]

print(_config)
print(load_db(_config))

@app.get("/")
async def start():
    """Entry point"""
    load_db(_config)
    return {"res": f"Hello from api module.", "config": _config}

@app.get("/init/db/{collection}")
async def init_db(collection: str):
    """Insère un document test pour s'assurer que la base et la collection existent."""
    sample_doc = {"name": "Test", "value": 42}
    get_collection(load_db(_config), collection).insert_one(sample_doc)
    return {"res": "Database and collection initialized !"}

@app.post("/write/db/{collection}")
async def write_data(data: dict, collection: str):
    """Ajoute un document dans MongoDB."""
    get_collection(load_db(_config), collection).insert_one(data)
    return {"res": f"( {len(data)} ) elts inserted !"}

@app.get("/read/db/{collection}")
async def read_data(collection: str):
    """Récupère tous les documents de MongoDB."""
    data = list(get_collection(load_db(_config), collection).find({}, {"_id": 0}))  # exclure l'ID mongo
    return {"res": {"data": data}}
