import logging
from psycopg2 import sql
from typing import List, Dict
from api_utils.commons import Connexion, ConnexionType


class LogementsDAO:
    """
    Implemente la classe Connexion (pattern de composition)
    pour se connecter et exécuter des requetes sur la table logements
    """
    def __init__(self, *args, **kwargs) -> None:
        self.conn = Connexion(target=ConnexionType.POSTGRESQL).get_conn(*args, **kwargs)
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()
        self.table_name = "logements"

    def select_all(self) -> List[Dict]:
        """
        Select all logements from the database.
        """
        try:
            res = self.cursor.execute(
                sql.SQL("SELECT * FROM {};").format(sql.Identifier(self.table_name))
                )
            res, excp = self.cursor.fetchall(), None
            res = [dict(zip([desc[0] for desc in self.cursor.description], row)) for row in res]
            logging.info("(ok) select from logements dao..")
        except Exception as e:
            res, excp = None, str(e)
            logging.info("(ko) select from logements dao..")
        finally:
            return res, excp
        

    def select_all_from_logements_by_adress(self, searched: str) -> List[Dict]:
        """
        Select all from data from logement with adress (label_ademe).
        :param searched: the searched address
        :return: all data from logement
        """
        try:
            query = sql.SQL("""
                SELECT l.* FROM {} as l
                LEFT JOIN adresses AS a on l._id_ademe = a._id_ademe
                WHERE LOWER(a.label_ban) LIKE LOWER(%s);
            """).format(sql.Identifier(self.table_name))
            self.cursor.execute(query, [f"%{searched}%"])
            res, excp = self.cursor.fetchall(), None
            res = [dict(zip([desc[0] for desc in self.cursor.description], row)) for row in res]
            logging.info("(ok) select similar from logementss dao..")
        except Exception as e:
            res, excp = None, str(e)
            logging.info("(ko) select similar from logementss dao..")
        finally:
            return res, excp
        
        
    def select_all_from_logements_by_city_name(self, city_name: str, nrows: int = -1) -> List[Dict]:
        """
        Select all logements from the database by city name.
        :param city_name: the name of the city
        :return: a list of logements in the city
        """
        try:
            if nrows > 0:
                query = sql.SQL("""
                    SELECT l.* FROM {} AS l
                    LEFT JOIN adresses AS a ON l.id_ban = a.id_ban
                    WHERE LOWER(a.city_ban) LIKE LOWER(%s)
                    LIMIT %s;
                """).format(sql.Identifier(self.table_name))
                self.cursor.execute(query, [f"%{city_name}%", nrows])
            else:
                query = sql.SQL("""
                    SELECT l.* FROM {} AS l
                    LEFT JOIN adresses AS a ON l.id_ban = a.id_ban
                    WHERE LOWER(a.city_ban) LIKE LOWER(%s);
                """).format(sql.Identifier(self.table_name))
                self.cursor.execute(query, [f"%{city_name}%"])
            res, excp = self.cursor.fetchall(), None
            res = [dict(zip([desc[0] for desc in self.cursor.description], row)) for row in res]
            logging.info("(ok) select logements by city name from logements dao..")
        except Exception as e:
            res, excp = None, str(e)
            logging.info("(ko) select logements by city name from logements dao..")
        finally:
            return res, excp
        