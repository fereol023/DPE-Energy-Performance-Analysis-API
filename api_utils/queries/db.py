import psycopg2, os
from psycopg2 import sql
from api_utils.commons import get_env_variable


def create_database_and_roles(
        conn, # conn as admin
        DATABASE_NAME,
        READER_ROLE,
        READER_PASSWORD,
        WRITER_ROLE,
        WRITER_PASSWORD
):
    try:
        # connect to the default 'postgres' database as an admin
        conn.autocommit = True
        cursor = conn.cursor()

        # create the database
        cursor.execute(sql.SQL("CREATE DATABASE {};").format(sql.Identifier(DATABASE_NAME)))

        # create roles
        cursor.execute(sql.SQL("CREATE ROLE {} WITH LOGIN PASSWORD %s;").format(sql.Identifier(READER_ROLE)), [READER_PASSWORD])
        cursor.execute(sql.SQL("CREATE ROLE {} WITH LOGIN PASSWORD %s;").format(sql.Identifier(WRITER_ROLE)), [WRITER_PASSWORD])

        # and grant permissions
        cursor.execute(sql.SQL("GRANT CONNECT ON DATABASE {} TO {}, {};").format(
            sql.Identifier(DATABASE_NAME),
            sql.Identifier(READER_ROLE),
            sql.Identifier(WRITER_ROLE)
        ))
        # TODO: toutes les tables de la base
        # evolution : restreindre les permissions sur la table des adresses
        cursor.execute(sql.SQL("GRANT SELECT ON ALL TABLES IN SCHEMA public TO {};").format(sql.Identifier(READER_ROLE)))
        cursor.execute(sql.SQL("GRANT INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO {};").format(sql.Identifier(WRITER_ROLE)))

        print("Database and roles created successfully.")
    except Exception as e:
        if "already exists" in str(e):
            print("Database already exists.")
        else:
            print(f"Error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def create_table(conn, query, params=None, comment=None):
    """
    Execute a SQL table creation query and return the result.
    """
    cursor = conn.cursor()
    try:
        cursor.execute(query, params) # la query peut etre un truc sql.identifier
        if cursor.description:  # check if the query returns rows
            return cursor.fetchall()
        else:
            conn.commit()  # commit changes for INSERT/UPDATE/DELETE queries
        if comment:
            print(f"Table created successfully with comment: {comment}")
    except Exception as e:
        if "already exists" in str(e):
            print(str(e))
        else:
            raise Exception(f"Error executing query: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()