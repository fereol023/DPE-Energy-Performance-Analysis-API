import logging
from psycopg2 import sql
from typing import List, Dict
from api_utils.commons import Connexion, ConnexionType


class AdressesDAO:
    """
    Implemente la classe Connexion (pattern de composition)
    pour se connecter et exécuter des requetes sur la table adresse
    """
    def __init__(self, *args, **kwargs) -> None:
        self.conn = Connexion(target=ConnexionType.POSTGRESQL).get_conn(*args, **kwargs)
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()
        self.table_name = "adresses"

    def select_all(self) -> List[Dict]:
        """
        Select all addresses from the database.
        """
        try:
            res = self.cursor.execute(
                sql.SQL("SELECT * FROM {};").format(sql.Identifier(self.table_name))
                )
            res, excp = self.cursor.fetchall(), None
            logging.info("(ok) select from adresses dao..")
        except Exception as e:
            res, excp = None, str(e)
            logging.info("(ko) select from adresses dao..")
        finally:
            return res, excp
        
    def select_all_adresses_labels(self) -> List[str]:
        """
        Select all addresses labels from the database.
        :return: a list of addresses labels
        """
        try:
            query = sql.SQL("SELECT label_ban FROM {};").format(sql.Identifier(self.table_name))
            self.cursor.execute(query)
            res, excp = [row[0] for row in self.cursor.fetchall()], None
            logging.info("(ok) select adresses labels from adresses dao..")
        except Exception as e:
            res, excp = None, str(e)
            logging.info("(ko) select adresses labels from adresses dao..")
        finally:
            return res, excp

    def select_one_adress(self, searched: str) -> List[Dict]:
        """
        Select all from addresses from searched one.
        :param searched: the searched address
        :return: all data from the searched address
        """
        try:
            query = sql.SQL("""
                SELECT * 
                FROM {} 
                WHERE LOWER(label_ban) LIKE LOWER(%s);
                """).format(sql.Identifier(self.table_name))
            self.cursor.execute(query, [f"%{searched}%"])
            res, excp = self.cursor.fetchall(), None
            logging.info("(ok) select similar from adresses dao..")
        except Exception as e:
            res, excp = None, str(e)
            logging.info("(ko) select similar from adresses dao..")
        finally:
            return res, excp
        
    def select_cities_names_and_codes(self) -> List[Dict]:
        """
        Select all city names and codes from the database.
        :return: a list of dictionaries with city names and codes
        """
        try:
            query = sql.SQL("""
                SELECT DISTINCT city_ban, code_departement_enedis, code_postal_ban_ademe 
                FROM {};
                """).format(sql.Identifier(self.table_name))
            self.cursor.execute(query)
            res, excp = self.cursor.fetchall(), None
            logging.info("(ok) select city names and codes from adresses dao..")
        except Exception as e:
            res, excp = None, str(e)
            logging.info("(ko) select city names and codes from adresses dao..")
        finally:
            return res, excp