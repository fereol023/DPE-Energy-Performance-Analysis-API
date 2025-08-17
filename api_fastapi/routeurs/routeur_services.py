from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import RedirectResponse
from api_utils.commons import get_env_variable

from minio import Minio
from minio.error import S3Error
import os, io, asyncio

router = APIRouter(tags=['micro-services'])

def get_s3_client():
    # set up MinIO client
    MINIO_ENDPOINT = get_env_variable("S3_ENDPOINT_URL")
    MINIO_ACCESS_KEY = get_env_variable("S3_ACCESS_KEY")
    MINIO_SECRET_KEY = get_env_variable("S3_SECRET_KEY")
    return Minio(
        MINIO_ENDPOINT,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=False  # True if using HTTPS
    )

# @router.get("/kibana-monitoring")
# async def redirect_logger_kibana():
#     """redirects to kibana page"""
#     KIBANA_HOST = get_env_variable('KIBANA_HOST', compulsory=False)
#     KIBANA_PORT = get_env_variable('KIBANA_PORT', compulsory=False, cast_to_type=int)

#     url = f"http://{KIBANA_HOST}:{KIBANA_PORT}"
#     try:
#         return RedirectResponse(f"{url}")
#     except:
#         raise HTTPException(status_code=500, detail="kibana dashboard is ko")

@router.get("/prefect/ping")
async def redirect_prefect_server():
    return 

@router.get("/prefect-server/dashboard")
async def redirect_prefect_server():
    return 


@router.get("/s3/ping")
async def ping_minio():
    try:
        minio_client = get_s3_client()
        MINIO_BUCKET_NAME = get_env_variable("S3_BUCKET_NAME")
        # make sure the bucket exists
        if not minio_client.bucket_exists(MINIO_BUCKET_NAME):
            minio_client.make_bucket(MINIO_BUCKET_NAME)
        # check connexion
        minio_client.list_buckets()
        return {"message": "MinIO connection is up."}
    except S3Error as e:
        raise HTTPException(status_code=500, detail=f"MinIO connection error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


@router.post("/s3/upload-file")
async def upload_csv(file: UploadFile):
    # validate file type
    if file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")
    
    try:
        # Read file data
        file_data = await file.read()
        file_name = file.filename
        minio_client = get_s3_client()
        MINIO_BUCKET_NAME = get_env_variable("S3_BUCKET_NAME")
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
