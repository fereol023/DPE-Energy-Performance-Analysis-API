import os
import redis
import secrets
import smtplib
import importlib
import pandas as pd
from typing import List
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from pydantic import BaseModel, EmailStr

from fastapi.security import OAuth2PasswordBearer
from fastapi import status, Response, APIRouter, Request, Depends, HTTPException

from api_utils.fonctions import load_pickle
from api_fastapi.exceptions import my_exception_handler 
from api_utils.controller import dbC, adressesC, logementsC
from ressources.models.v1.model_config import InputModel as InputModelv1


redis_client = redis.Redis(host=os.getenv('REDIS_HOST'), port=int(os.getenv('REDIS_PORT')), db=0, decode_responses=True)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login-with-otp")

class OTPRequest(BaseModel):
    email: EmailStr

class OTPLogin(BaseModel):
    email: EmailStr
    otp: str

def get_current_user(token: str = Depends(oauth2_scheme)):
    """dependance : Vérifie le token"""
    role = redis_client.get(f"token:{token}")
    if not role:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide ou expiré")
    return {"role": role}

def require_role(required_role: list[str]):
    def role_checker(user: dict = Depends(get_current_user)):
        """
        Vérifie si l'utilisateur possède le rôle requis.
        """
        if user.get("role") not in required_role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès interdit")
        return user
    return role_checker

router = APIRouter(
    prefix="",
    tags=['database'],
    dependencies=[Depends(get_current_user)]
)

auth_router = APIRouter(
    prefix="",
    tags=['auth'],
)

@auth_router.post("/send-otp")
def send_otp(request: OTPRequest):
    """
    Génère un OTP, le stocke dans Redis avec TTL, et l'envoie par email.
    """
    otp = str(secrets.randbelow(100000)).zfill(5)
    redis_client.setex(f"otp:{request.email}", 300, otp)  # TTL: 5 min

    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = int(os.getenv("SMTP_PORT")) # protocole TLS 587 ssl 465(gmail)
    SMTP_USERNAME = os.getenv("SMTP_USERNAME") 
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

    subject = "Votre code OTP"
    body = f"Votre code OTP est : {otp}\nCe code est valable 5 minutes."
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_USERNAME
    msg["To"] = request.email

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_USERNAME, request.email, msg.as_string())
            return {"message": f"OTP envoyé à {request.email} : {body}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur SMTP : {str(e)}")


@auth_router.post("/login-with-otp")
def login_with_otp(data: OTPLogin, response: Response):
    """
    Vérifie email + OTP dans Redis, assigne rôle et durée de cookie.
    :returns message with token inside, useful for streamlit to post treat,
    can also set directly to client
    """
    stored_otp = redis_client.get(f"otp:{data.email}")
    if not stored_otp or stored_otp != data.otp:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="OTP invalide ou expiré")
    # Définir rôle et TTL cookie
    if data.email.lower() == os.getenv("ADMIN_EMAIL", "habzjhzh"):
        role = "admin"
        expiry = 30  # minutes
    else:
        role = "reader"
        expiry = 60  # minutes
    # générer token
    token = secrets.token_urlsafe(32)
    redis_client.setex(f"token:{token}", expiry * 60, role)
    # poser cookie HTTPOnly
    expire_date = datetime.utcnow() + timedelta(minutes=expiry)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=expiry * 60,
        expires=expiry * 60,
        secure=False,  # à mettre True en prod avec HTTPS
        samesite="Strict"
    )
    return {"access_token": token, "token_type": "bearer", "role": role}


@auth_router.get("/user-status")
def get_user(user=Depends(get_current_user)):
    if user["role"] not in ["reader", "admin"]:
        raise HTTPException(status_code=403, detail="Accès refusé")
    return {"message": f"Données accessibles par {user['role']}"}


################
###   Router bdd
#################
@router.get("/db")
async def init_db_require_admin_level_access(user: dict = Depends(require_role(["admin"]))):
    try:
        dbC.init()
        state = "ready"
    except Exception as e:
        state = f"Database KO with exception : {e}"
        raise e
    finally:
        return {
            "message": "hello from db router !",
            "db state": state
        }

#### adresses 
@my_exception_handler
@router.get("/db/reader/adresses/getall")
async def get_all_adresses_require_admin_level_access(request: Request, user: dict = Depends(require_role(["admin"]))):
    rep, exp = adressesC.get_all_adresses()
    return {"data": rep, "error": exp}


@my_exception_handler
@router.get("/db/reader/adresses/searchadress/{searched}")
async def search_similar_adresses_require_reader_level_access(request: Request, searched: str, user: dict = Depends(require_role(["reader", "admin"]))):
    """
    Get all adresses similar to the searched one.
    :param searched: the searched address
    :return: a list of similar addresses
    """
    rep, exp = adressesC.search_adress(searched)
    return {"data": rep, "error": exp}


@my_exception_handler
@router.get("/db/reader/adresses/getone/{searched_adress}")
async def get_one_adresses_require_reader_level_access(request: Request, searched_adress: str, user: dict = Depends(require_role(["reader", "admin"]))):
    """
    Get all adresses similar to the searched one.
    :param searched: the searched address
    :return: a list of similar addresses
    """
    # validate adress format
    if searched_adress and len(searched_adress) > 3:
        rep, exp = adressesC.get_one_adress(searched_adress)
        return {"data": rep, "error": exp}
    else:
        raise HTTPException(status_code=400, detail="Searched address must be at least 3 characters long.")


@my_exception_handler
@router.get("/db/reader/adresses/cities")
async def get_cities_names_and_codes_reader_level(request: Request, user: dict = Depends(require_role(["reader", "admin"]))):
    """
    Get all cities names and codes from the database.
    :return: a list of cities names and codes
    """
    rep, exp = adressesC.get_cities_names_and_codes()
    return {"data": rep, "error": exp}

@my_exception_handler
@router.get("/db/reader/adresses/{city_name}/allcoords")
async def get_coord_by_city_name_reader_level(request: Request, city_name: str, user: dict = Depends(require_role(["reader", "admin"]))):
    """
    Get longitudes, latitudes by city name.
    :return: a list of cities names
    """
    rep, exp = adressesC.get_coord_by_city_name(city_name)
    return {"data": rep, "error": exp}


#### logements
@my_exception_handler
@router.get("/db/reader/logements/getall")
async def get_all_logements_reader_level(request: Request, user: dict = Depends(require_role(["reader", "admin"]))):
    """
    Get all logements from the database
    :return: list of logements
    """
    rep, exp = logementsC.get_all_logements()
    return {"data": rep, "error": exp}

@my_exception_handler
@router.get("/db/reader/logements/getbyadress/{searched}")
async def get_logements_by_adress_reader_level(request: Request, searched: str, user: dict = Depends(require_role(["reader", "admin"]))):
    """
    Get all logements from the database by address (label_ademe).
    :param searched: the searched address
    :return: a list of logements in the address
    """
    rep, exp = logementsC.get_logements_by_adress(searched)
    return {"data": rep, "error": exp}

@my_exception_handler
@router.get("/db/reader/logements/getonebycity/{city_name}")
async def get_one_logements_by_city_name(request: Request, city_name: str):
    """
    Get only one logement from the database by city name.
    Example case for the model page.
    :param city_name: the name of the city
    :return: a list of logements in the city
    """
    rep, exp = logementsC.get_logements_by_city_name(city_name, nrows=1)
    return {"data": rep, "error": exp}

@my_exception_handler
@router.get("/db/reader/logements/getallbycity/{city_name}")
async def get_all_logements_by_city_name(request: Request, city_name: str):
    """
    Get all logements from the database by city name.
    :param city_name: the name of the city
    :return: a list of logements in the city
    """
    rep, exp = logementsC.get_logements_by_city_name(city_name, nrows=-1)
    return {"data": rep, "error": exp}

#### model
@router.get("/model/{version}/config", tags=["model 🤖"])
async def get_model_config(version):
    module = importlib.import_module(f"ressources.models.{version}.model_config")
    return module.model_config

@router.post("/model/v1/predict", tags=["model 🤖"])
async def predict(data: List[InputModelv1]):
    try:
        df = pd.DataFrame([item.dict() for item in data]).sort_index(axis=1)
        model = load_pickle('ressources/models/v1/RF3_new_version_wo_vd.pkl', is_optional=False)
        df = df[model.feature_names_in_]
        predictions = model.predict(df)
        return {'predictions': predictions.tolist(), 'error': []}
    except Exception as e:
        return {'predictions': [], 'error': str(e)}
