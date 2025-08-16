import os
from api_utils.commons import Connexion, ConnexionType
from api_utils.queries import (
    db as db_queries,
    adresses as adresses_queries,
    logements as logements_queries,
    villes as villes_queries,
    donnees_climatiques as donnees_climatiques_queries,
    donnees_geocodage as donnees_geocodage_queries,
    tests_statistiques_dpe as tests_statistiques_dpe_queries,
)
from api_utils.commons import get_env_variable
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


# db connexion parameters
HOST = get_env_variable("POSTGRES_HOST")
PORT = get_env_variable("POSTGRES_PORT")
DATABASE_NAME = get_env_variable("POSTGRES_DB_NAME")

# reader and writer credentials
ADMIN_USERNAME = get_env_variable("POSTGRES_ADMIN_USERNAME")
ADMIN_PASSWORD = get_env_variable("POSTGRES_ADMIN_PASSWORD")
READER_ROLE = get_env_variable("POSTGRES_READER_USERNAME")
READER_PASSWORD = get_env_variable("POSTGRES_READER_PASSWORD")
WRITER_ROLE = get_env_variable("POSTGRES_WRITER_USERNAME")
WRITER_PASSWORD = get_env_variable("POSTGRES_WRITER_PASSWORD")


def create_db_if_not_exists():
    try:
        # Connect to the default 'postgres' database to check/create target db
        conn = psycopg2.connect(
            dbname="postgres", 
            # doit se connecter à la base de données par défaut 
            # et utiliser la connexion pour checker la base à créer
            user=ADMIN_USERNAME,
            password=ADMIN_PASSWORD,
            host=HOST,
            port=PORT
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DATABASE_NAME}'")
        exists = cur.fetchone()
        if not exists:
            cur.execute(f"CREATE DATABASE {DATABASE_NAME}")
            print(f"Database '{DATABASE_NAME}' created.")
        else:
            print(f"Database '{DATABASE_NAME}' already exists.")
        cur.close()
        conn.close()
    except Exception as e:
        raise Exception(f"Error ensuring database exists: {e}")


def init():
    """
    Initialize the database.
    :return: None
    """

    create_db_if_not_exists()

    # db and roles
    db_queries.create_database_and_roles(
        conn=Connexion(ConnexionType.POSTGRESQL).get_conn(),
        DATABASE_NAME=DATABASE_NAME,
        READER_ROLE=READER_ROLE,
        READER_PASSWORD=READER_PASSWORD,
        WRITER_ROLE=WRITER_ROLE,
        WRITER_PASSWORD=WRITER_PASSWORD
    )

    # create tables
    if get_env_variable("VERBOSE", default_value="1", compulsory=True, cast_to_type=int)==1:
        print("Starting creating tables...")
    migrations = [
        (adresses_queries.create_table, "create adresses table"), # contraintes d'integrité
        (villes_queries.create_table, "create villes table"),
        (donnees_climatiques_queries.create_table, "create donnees_climatiques table"),
        (donnees_geocodage_queries.create_table, "create donnees_geocodage table"),
        (tests_statistiques_dpe_queries.create_table, "create tests_statistiques_dpe table"),
        (logements_queries.create_table, "create logements table"),
    ]

    try:
        for query, comment in migrations:
            db_queries.create_table(Connexion(ConnexionType.POSTGRESQL).get_conn(), query, comment)
        if get_env_variable("VERBOSE", default_value="1", compulsory=True, cast_to_type=int)==1:
            print("All tables created successfully.")
    except Exception as e:
        raise Exception(f"Error while creating tables {comment} : {e}")
    


