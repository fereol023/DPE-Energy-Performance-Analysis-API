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


@my_exception_handler
@router.get("/ping-all-services", tags=["🙋‍♂️ health check"])
async def ping_all_services():
    """
    Single endpoint to ping all microservices used by the API.
    - redis
    - s3 (minio)
    - prefect server
    - postgres db
    """
    results = {}
    # ping redis
    try:
        import redis
        redis_client = redis.Redis(host=os.getenv('REDIS_HOST'), port=int(os.getenv('REDIS_PORT')), db=0, decode_responses=True)
        s = time.time()
        pong = redis_client.ping()
        f = round((time.time()-s) * 1_000, 2) # en ms
        results['Redis Server (caching service)'] = f"""
        - Status": {"✅ ok" if pong else "❌ ko"}
        - Elapsed": {f} ms
        """
    except Exception as e:
        results['redis'] = {
            "status": "❌ ko",
            "error": str(e)
        }

    # ping s3
    try:
        s3_client = get_s3_client()
        bucket_name = get_env_variable("S3_BUCKET_NAME")
        s = time.time()
        s3_client.head_bucket(Bucket=bucket_name)
        f = round((time.time()-s) * 1_000, 2) # en ms
        results['S3 API (object storage)'] = f"""
        - Status: ✅ ok
        - Elapsed": {f} ms
        """
    except Exception as e:
        results['s3'] = {
            "status": "❌ ko",
            "error": str(e)
        }
    
    # ping prefect server
    try:
        p = get_env_variable('PREFECT_API_URL')
        s = time.time()
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(p)
        f = round((time.time()-s) * 1_000, 2) # en ms
        results['Prefect Server (orchestrator)'] = f"""
        - Status_code : {response.status_code} 
        - Elapsed : ✅ {f} ms 
        - Ok : {response.status_code == 200}
        """
    except Exception as e:
        results['prefect_server'] = {
            "status": "❌ ko",
            "error": str(e)
        }

    # ping postgres
    try:
        import psycopg2
        POSTGRES_HOST = get_env_variable("POSTGRES_HOST")
        POSTGRES_PORT = get_env_variable("POSTGRES_PORT")
        POSTGRES_DB_NAME = get_env_variable("POSTGRES_DB_NAME")
        POSTGRES_ADMIN_USERNAME = get_env_variable("POSTGRES_ADMIN_USERNAME")
        POSTGRES_ADMIN_PASSWORD = get_env_variable("POSTGRES_ADMIN_PASSWORD")

        s = time.time()
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database=POSTGRES_DB_NAME,
            user=POSTGRES_ADMIN_USERNAME,
            password=POSTGRES_ADMIN_PASSWORD
        )
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        cur.fetchone()
        cur.close()
        conn.close()
        f = round((time.time()-s) * 1_000, 2) # en ms
        results['Postgres Server (database)'] = f"""
        - Status : ✅ ok 
        - Elapsed": {f} ms
        """
    except Exception as e:
        results['postgres'] = {
            "status": "❌ ko",
            "error": str(e)
        }
    
    # send back results through smtp server
    try:
        import smtplib
        from email.mime.text import MIMEText

        SMTP_SERVER = os.getenv("SMTP_SERVER")
        SMTP_PORT = int(os.getenv("SMTP_PORT")) # protocole TLS 587 ssl 465(gmail)
        SMTP_USERNAME = os.getenv("SMTP_USERNAME") 
        SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
        ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")

        subject = "Microservices Health Check Report"
        body = "Voici le rapport de santé des microservices :\n\n"
        for service, result in results.items():
            body += f"{service} : {result}\n"
        
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = SMTP_USERNAME
        msg["To"] = ADMIN_EMAIL

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_USERNAME, ADMIN_EMAIL, msg.as_string())
    except Exception as e:
        results['smtp'] = {
            "status": "❌ ko",
            "error": str(e)
        }
    return results


@my_exception_handler
@router.get("/mailing-users")
def mailing_users(mail_content: str = "This is a notification email to all registered users."):
    """sends an email to all users in the db"""
    try:
        import smtplib
        from email.mime.text import MIMEText
        users = get_users_from_db(postgres=False)

        if not users:
            return {"message": "No users found in the database."}

        # send email to all users
        SMTP_SERVER = os.getenv("SMTP_SERVER")
        SMTP_PORT = int(os.getenv("SMTP_PORT")) # protocole TLS 587 ssl 465(gmail)
        SMTP_USERNAME = os.getenv("SMTP_USERNAME") 
        SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

        subject = "Notification to all users"
        body, _ = parse_mail_content(mail_content)

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = SMTP_USERNAME
        msg["To"] = ", ".join(users)

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_USERNAME, users, msg.as_string())

        return {"message": f"Email sent to {len(users)} users."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {str(e)}")
    

def parse_mail_content(content):
    return content, True

def get_users_from_db(postgres=True):
    if not postgres:
        # mock users
        # load from file txt
        try:
            import pathlib, os
            root_dir = pathlib.Path(__file__).parent.parent.parent.resolve()
            file_path = os.path.join(root_dir, "users.txt")
            with open(file_path, "r") as f:
                return f.read().splitlines()            
        except Exception as e:
            return []
    else:
        try:
            import psycopg2
            POSTGRES_HOST = get_env_variable("POSTGRES_HOST")
            POSTGRES_PORT = get_env_variable("POSTGRES_PORT")
            POSTGRES_DB_NAME = get_env_variable("POSTGRES_DB_NAME")
            POSTGRES_ADMIN_USERNAME = get_env_variable("POSTGRES_ADMIN_USERNAME")
            POSTGRES_ADMIN_PASSWORD = get_env_variable("POSTGRES_ADMIN_PASSWORD")

            conn = psycopg2.connect(
                host=POSTGRES_HOST,
                port=POSTGRES_PORT,
                database=POSTGRES_DB_NAME,
                user=POSTGRES_ADMIN_USERNAME,
                password=POSTGRES_ADMIN_PASSWORD
            )
            cur = conn.cursor()
            cur.execute("SELECT email FROM users;")
            rows = cur.fetchall()
            users = [row[0] for row in rows]
            cur.close()
            conn.close()
            return users
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error occurred: {str(e)}")