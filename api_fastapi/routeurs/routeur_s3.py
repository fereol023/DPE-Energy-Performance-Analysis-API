from fastapi import APIRouter, UploadFile, HTTPException
from minio import Minio
from minio.error import S3Error
import os, io, asyncio

from api_utils.commons import get_env_variable

router = APIRouter()

# config MinIO client
MINIO_ENDPOINT = get_env_variable("S3_ENDPOINT_URL")
MINIO_ACCESS_KEY = get_env_variable("S3_ACCESS_KEY")
MINIO_SECRET_KEY = get_env_variable("S3_SECRET_KEY")
MINIO_BUCKET_NAME = get_env_variable("S3_BUCKET_NAME")

try:
    minio_client = Minio(
        MINIO_ENDPOINT,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=False  # True if using HTTPS
    )
except Exception as e:
    print(f"Erreur connexion fs : {e}")

# make sure the bucket exists
if not minio_client.bucket_exists(MINIO_BUCKET_NAME):
    minio_client.make_bucket(MINIO_BUCKET_NAME)

@router.get("/ping-minio", tags=["Filestorage S3 module"])
async def ping_minio():
    try:
        # check connexion
        minio_client.list_buckets()
        return {"message": "MinIO connection is up."}
    except S3Error as e:
        raise HTTPException(status_code=500, detail=f"MinIO connection error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


@router.post("/upload-input", tags=["Filestorage S3 module"])
async def upload_csv(file: UploadFile):
    # Validate file type
    if file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")
    
    try:
        # Read file data
        file_data = await file.read()
        file_name = file.filename
        
        # Save the file to MinIO
        minio_client.put_object(
            MINIO_BUCKET_NAME,
            file_name,
            data=io.BytesIO(file_data),
            length=len(file_data),
            content_type="text/csv"
        )
        await asyncio.sleep(1)
        return {"message": f"File '{file_name}' uploaded successfully to MinIO."}
    except S3Error as e:
        raise HTTPException(status_code=500, detail=f"MinIO error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
