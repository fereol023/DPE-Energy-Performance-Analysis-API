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
            res = self.cursor.fetchall(), None
            logging.info("(ok) select from adresses dao..")
        except Exception as e:
            res = None, str(e)
            logging.info("(ko) select from adresses dao..")
        finally:
            return res