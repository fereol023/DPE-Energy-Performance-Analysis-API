import os
from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/mydatabase")

client = MongoClient(MONGO_URI)
db = client["dpe_database"]
collection = db["test_collection"]

@app.get("/")
async def start():
    """Ajoute un document dans MongoDB."""
    return {"MSG": f"Hello from api module. Mongo db running on : {MONGO_URI}"}

@app.get("/init-db")
async def init_db():
    """Insère un document test pour s'assurer que la base et la collection existent."""
    sample_doc = {"name": "Test", "value": 42}
    collection.insert_one(sample_doc)
    return {"message": "Database and collection initialized !"}

@app.post("/write")
async def write_data(data: dict):
    """Ajoute un document dans MongoDB."""
    collection.insert_one(data)
    return {"res": f"( {len(data)} ) elts inserted !"}

@app.get("/read")
async def read_data():
    """Récupère tous les documents de MongoDB."""
    data = list(collection.find({}, {"_id": 0}))  # exclure l'ID mongo
    return {"data": data}
