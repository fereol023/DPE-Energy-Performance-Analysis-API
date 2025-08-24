import os
import io
import time
import boto3
import httpx
import asyncio

from fastapi.responses import RedirectResponse
from api_utils.commons import get_env_variable
from fastapi import APIRouter, HTTPException, UploadFile
from api_fastapi.exceptions import my_exception_handler 



router = APIRouter(tags=['micro-services'])

def get_s3_client():
    S3_ENDPOINT = get_env_variable("S3_ENDPOINT_URL")
    S3_ACCESS_KEY = get_env_variable("S3_ACCESS_KEY")
    S3_SECRET_KEY = get_env_variable("S3_SECRET_KEY")
    if S3_ENDPOINT:
        if not S3_ENDPOINT.startswith("http://"): S3_ENDPOINT = f"http://{S3_ENDPOINT}"
    return boto3.client(
        "s3",
        endpoint_url=S3_ENDPOINT, # optional def None
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_KEY,
        region_name="eu-west-3" # paris europe
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

@my_exception_handler
@router.get("/prefect/ping")
async def redirect_prefect_server():
    try:
        p = get_env_variable('PREFECT_API_URL')
        s = time.time()
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(p)
        f = round((time.time()-s) * 1_000, 2) # en ms
        return {
            "url": p,
            "status_code": response.status_code,
            "elapsed": f"{f} ms",
            "ok": response.status_code == 200
        }
    except Exception as e:
        raise Exception(f"Exception with url {p} : {str(e)}")

@my_exception_handler
@router.get("/prefect-server/dashboard")
async def redirect_prefect_server():
    p = get_env_variable('PREFECT_UI_URL')
    return RedirectResponse(p)

@my_exception_handler
@router.get("/s3/ping")
async def ping_s3():
    try:
        s3_client = get_s3_client()
        bucket_name = get_env_variable("S3_BUCKET_NAME")
        s3_client.head_bucket(Bucket=bucket_name)
        return {"message": "MinIO connection is up."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"S3 connexion error occurred: {str(e)}")

@my_exception_handler
@router.post("/s3/upload-file")
async def upload_csv(file: UploadFile):
    # validate file type
    # TODO 
    return