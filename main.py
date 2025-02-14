from fastapi import FastAPI
from pymongo import MongoClient
import os

app = FastAPI()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/mydatabase")
client = MongoClient(MONGO_URI)
db = client.mydatabase
collection = db.mycollection

@app.post("/write/")
async def write_data(data: dict):
    """Ajoute un document dans MongoDB."""
    result = collection.insert_one(data)
    return {"inserted_id": str(result.inserted_id)}

@app.get("/read/")
async def read_data():
    """Récupère tous les documents de MongoDB."""
    data = list(collection.find({}, {"_id": 0}))  # exclure l'ID MongoDB
    return {"data": data}
