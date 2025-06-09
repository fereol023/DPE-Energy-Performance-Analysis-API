import os, importlib
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Request, Depends, HTTPException

from api_fastapi.exceptions import (
    my_exception_handler, 
    validate_reader_handler
)
from api_fastapi import (
    create_reader_jwt_token, 
    validate_reader_identity_simple,
    validate_reader_identity
)
from api_utils.controller import dbC, adressesC, logementsC


router = APIRouter()

_bdd_tag = ["BDD"]
_logements_tag = ["Logements"]
_adresses_tag = ["Adresses"]

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
    """
    Placeholder // no more implemented because
    etl engine uses sqlalchemy driectly to 
    write in the database (31/05/25)
    ----
    maybe evolution to a writer role
    for the app client to write in the database.
    """
    pass


#### adresses 
@my_exception_handler
@validate_reader_handler # hide underneath complexity of token validation inside decorator
@router.get("/db/reader/adresses/getall", tags=_bdd_tag+_adresses_tag)
async def get_all_adresses(request: Request):
    rep, exp = adressesC.get_all_adresses()
    return {"data": rep, "error": exp}


@my_exception_handler
@validate_reader_handler
@router.get("/db/reader/adresses/searchadress/{searched}", tags=_bdd_tag+_adresses_tag)
async def search_adresses(request: Request, searched: str):
    """
    Get all adresses similar to the searched one.
    :param searched: the searched address
    :return: a list of similar addresses
    """
    rep, exp = adressesC.search_adress(searched)
    return {"data": rep, "error": exp}


@my_exception_handler
@validate_reader_handler
@router.get("/db/reader/adresses/getone/{searched_adress}", tags=_bdd_tag+_adresses_tag)
async def search_adresses(request: Request, searched_adress: str):
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
@validate_reader_handler
@router.get("/db/reader/adresses/cities", tags=_bdd_tag+_adresses_tag)
async def get_cities_names_and_codes(request: Request):
    """
    Get all cities names and codes from the database.
    :return: a list of cities names and codes
    """
    rep, exp = adressesC.get_cities_names_and_codes()
    return {"data": rep, "error": exp}

@my_exception_handler
@validate_reader_handler
@router.get("/db/reader/adresses/{city_name}/allcoords", tags=_bdd_tag+_adresses_tag)
async def get_coord_by_city_name(request: Request, city_name: str):
    """
    Get longitudes, latitudes by city name.
    :return: a list of cities names
    """
    rep, exp = adressesC.get_coord_by_city_name(city_name)
    return {"data": rep, "error": exp}


#### logements
@my_exception_handler
@validate_reader_handler
@router.get("/db/reader/logements/getall", tags=_bdd_tag+_logements_tag)
async def get_all_logements(request: Request):
    """
    Get all logements from the database
    :return: list of logements
    """
    rep, exp = logementsC.get_all_logements()
    return {"data": rep, "error": exp}

@my_exception_handler
@validate_reader_handler
@router.get("/db/reader/logements/getbyadress/{searched}", tags=_bdd_tag+_logements_tag)
async def get_logements_by_adress(request: Request, searched: str):
    """
    Get all logements from the database by address (label_ademe).
    :param searched: the searched address
    :return: a list of logements in the address
    """
    rep, exp = logementsC.get_logements_by_adress(searched)
    return {"data": rep, "error": exp}

@my_exception_handler
@validate_reader_handler
@router.get("/db/reader/logements/getonebycity/{city_name}", tags=_bdd_tag+_logements_tag)
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
@validate_reader_handler
@router.get("/db/reader/logements/getallbycity/{city_name}", tags=_bdd_tag+_logements_tag)
async def get_all_logements_by_city_name(request: Request, city_name: str):
    """
    Get all logements from the database by city name.
    :param city_name: the name of the city
    :return: a list of logements in the city
    """
    rep, exp = logementsC.get_logements_by_city_name(city_name, nrows=-1)
    return {"data": rep, "error": exp}

# TODO:
## get all logements by city and arrondissement -> add filter on arr
## get all logements by city and arrondissement and data year -> add filter on arr
## get only consommations by city -> use to plot distribution train vs history 
## send schema of both tables logements and adresses -> schema for batch mode

#### model
@router.get("/model/{version}/config")
async def get_model_config(version):
    module = importlib.import_module(f"ressources.models.{version}.model_config")
    return module.model_config
