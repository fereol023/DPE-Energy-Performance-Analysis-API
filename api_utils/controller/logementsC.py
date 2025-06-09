from api_utils.dao.logementsDAO import LogementsDAO
from api_utils.controller import adressesC


def get_all_logements(*args, **kwargs):
    """
    Get all logements from the database
    :return: list of logements
    """
    rep, exp = LogementsDAO(*args, **kwargs).select_all()
    if exp: 
        return [], exp
    return rep, exp


def get_logements_by_adress(searched: str, *args, **kwargs):
    """
    Get all logements from the database by address (label_ademe).
    :param searched: the searched address
    :return: a list of logements in the address
    """
    rep, exp = LogementsDAO(*args, **kwargs)\
        .select_all_from_logements_by_adress(searched)
    if exp:
        return [], exp
    if not rep:
        return [], "No logements found for this address."
    return rep, exp

def get_logements_by_city_name(city_name: str, nrows: int, *args, **kwargs):
    """
    Get all logements from the database by city name.
    :param city_name: the name of the city
    :return: a list of logements in the city
    """
    rep, exp = LogementsDAO(*args, **kwargs)\
        .select_all_from_logements_by_city_name(city_name, nrows)
    if exp:
        return [], exp
    if not rep:
        return [], "No logements found for this city."
    return rep, exp
