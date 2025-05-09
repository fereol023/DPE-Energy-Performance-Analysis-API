import os
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse

from api_fastapi.exceptions import exception_handler, validate_reader_handler
from api_utils.controller import dbC
from api_fastapi import (
    create_reader_jwt_token, 
    validate_reader_identity_simple,
    validate_reader_identity
)
from api_utils.controller import adressesC

router = APIRouter()
_bdd_tag = ["BDD"]

@router.get("/db", tags=_bdd_tag)
async def init_db():
    try:
        dbC.init()
        state = "ready"
    except Exception as e:
        state = f"Database KO with exception : {e}"
    finally:
        return {
            "message": "hello from db router !",
            "reader-token": create_reader_jwt_token(), # generate cookie for client TODO ok
            "reader-token-validity-hours": os.getenv("JWT_TOKEN_EXPIRATION_HOURS", "1"),
            "db state": state
        }
    
#### log in
@router.get("/db/reader/", tags=_bdd_tag)
async def connect_as_reader():
    pass

@router.get("/db/writer/", tags=_bdd_tag)
async def connect_as_writer():
    pass


#### adresses 
@exception_handler
@validate_reader_handler # hide underneath complexity of token validation inside decorator
@router.get("/db/reader/adresses/getall", tags=_bdd_tag)
async def get_all_adresses(request: Request):
    rep, exp = adressesC.get_all_adresses()
    return {"data": rep, "error": exp}


@exception_handler
@validate_reader_handler
@router.get("/db/reader/adresses/getdpecount", tags=_bdd_tag)
async def get_adresse_dpe_counts():
    # rep, exp = adressesC.get_adresse_dpe_count()
    rep = {"label": ["A", "B", "C", "D", "E", "F", "G"], "count": [50, 200, 300, 250, 100, 150, 100]}
    exp = None
    return {"data": rep, "error": exp}



#### consommations electrique
@router.get("/db/reader/consos/avg/by/dpe", tags=_bdd_tag)
@exception_handler(if_error_status=500)
async def get_avg_conso_by_dpe():
    return # all consos (yc /m2) by dpe


@router.get("/db/client/deperditions/avg/by/dpe", tags=_bdd_tag)
@exception_handler
async def get_deperd_by_dpe():
    return # all depeditions avg group by dpe


#### logements
