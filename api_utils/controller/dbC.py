import os
from api_utils.commons import Connexion, ConnexionType
from api_utils.queries import (
    db as db_queries,
    adresses as adresses_queries,
    logements as logements_queries,
)
from api_utils.commons import get_env_variable


# db connexion parameters
HOST = get_env_variable("POSTGRES_HOST")
PORT = get_env_variable("POSTGRES_PORT")
DATABASE_NAME = get_env_variable("POSTGRES_DB_NAME")

# reader and writer credentials
READER_ROLE = get_env_variable("POSTGRES_READER_USERNAME")
READER_PASSWORD = get_env_variable("POSTGRES_READER_PASSWORD")
WRITER_ROLE = get_env_variable("POSTGRES_WRITER_USERNAME")
WRITER_PASSWORD = get_env_variable("POSTGRES_WRITER_PASSWORD")


def init():
    """
    Initialize the database.
    :return: None
    """
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
    if eval(get_env_variable("VERBOSE", "1"))==1:
        print("Starting creating tables...")
    migrations = [
        (logements_queries.create_table, "create logements table"),
        (adresses_queries.create_table, "create adresses table"), # contraintes d'integrité
    ]

    try:
        for query, comment in migrations:
            db_queries.create_table(Connexion(ConnexionType.POSTGRESQL).get_conn(), query, comment)
        if eval(get_env_variable("VERBOSE", "1"))==1:
            print("All tables created successfully.")
    except Exception as e:
        raise Exception(f"Error creating tables: {e}")