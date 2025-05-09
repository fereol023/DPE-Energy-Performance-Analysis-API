from api_utils.dao.adressesDAO import AdressesDAO


def get_all_adresses(*args, **kwargs):
    """
    Get all adresses from the database
    :return: list of adresses
    """
    rep, exp = AdressesDAO(*args, **kwargs).select_all()
    if exp: 
        return [], exp
    return rep, exp