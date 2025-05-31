from api_utils.dao.adressesDAO import AdressesDAO
from difflib import SequenceMatcher


def similar(a, b):
    """
    explicaton de ratio()
    Where T is the total number of elements in both sequences, 
    and M is the number of matches, this is 2.0*M / T. 
    Note that this is 1.0 if the sequences are identical, 
    and 0.0 if they have nothing in common.
    """
    return SequenceMatcher(None, a, b).ratio()


def get_all_adresses(*args, **kwargs):
    """
    Get all adresses from the database
    :return: list of adresses
    """
    rep, exp = AdressesDAO(*args, **kwargs).select_all()
    if exp: 
        return [], exp
    return rep, exp


def search_adress(searched: str="", threshold=0.8, *args, **kwargs):
    """
    Get all adresses similar to the searched one.
    :param searched: the searched address
    :return: a list of similar addresses
    """
    rep, exp = AdressesDAO(*args, **kwargs).select_all_adresses_labels()
    
    # rep = [addr.lower().replace(" ", "") for addr in rep]
    searched = searched.lower().replace(" ", "")

    # if searched is empty, return an empty list
    if (not rep) or exp:
        return [], exp    
    if not searched:
        return [], "No address provided for search."

    # compute similarity, map addresses to their similarity score
    similar_adresses = {}
    for addr in rep:
        k = addr.lower().replace(" ", "")
        s = round(similar(searched, k), 3)
        if s >= threshold:
            similar_adresses.update({k: [addr, s]})
    # sort by similarity score
    similar_adresses = sorted(similar_adresses.items(), key=lambda x: x[1][1], reverse=True)    
    if not similar_adresses:
        return [], "No similar addresses found."
    similar_adresses = [item[1] for item in similar_adresses]  # keep only the address and score
    return similar_adresses, exp
    

def get_one_adress(searched: str, *args, **kwargs):
    """
    Get all data from the searched address.
    :param searched: the searched address
    :return: all data from the searched address
    """
    rep, exp = AdressesDAO(*args, **kwargs).select_one_adress(searched)
    if exp:
        return [], exp
    if not rep:
        return [], "No address found."
    return rep, exp


def get_average_data_on_one_adress(searched: str, *args, **kwargs):
    """
    Get average data on one address.
    :param searched: the searched address
    :return: average data on the searched address
    """
    # placeholder 
    return {}, None


def count_logements_on_one_adress(searched: str, *args, **kwargs):
    return 0, None
