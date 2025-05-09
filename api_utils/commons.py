import os
import psycopg2
from enum import Enum


def get_env_variable(var_name, default=None):
    """Get the environment variable or raise an exception if default is not given."""
    try:
        return os.environ[var_name]
    except KeyError:
        if default is not None:
            return default
        else:
            raise EnvironmentError(f"Set the {var_name} environment variable")


class ConnexionType(Enum):
    POSTGRESQL = "postgresql"
    S3 = "s3"


class Connexion:
    def __init__(self, target: ConnexionType=None):
        self.target = self.__set_conn_target(target)

    def __set_conn_target(self, target):
        if target is None:
            raise Exception("Target cannot be None, please specify a target as ConnexionType")
        if isinstance(target, ConnexionType):
            return target
        else:
            raise Exception("Target must be ConnexionType, please specify a target as ConnexionType")
    
    def __get_conn_as_admin(self):
        if self.target == ConnexionType.POSTGRESQL:
            return psycopg2.connect(
                host=get_env_variable("POSTGRES_HOST"),
                database=get_env_variable("POSTGRES_DB_NAME"),
                user=get_env_variable("POSTGRES_ADMIN_USERNAME"),
                password=get_env_variable("POSTGRES_ADMIN_PASSWORD"),
                port=get_env_variable("POSTGRES_PORT"),
            )
        elif self.target == ConnexionType.S3:
            raise NotImplementedError("S3 connection not implemented yet")
        else:
            raise Exception("Target not supported")
    
    def get_conn(self, credentials: dict=None):
        """credentials : {username, password}, if None connects as admin"""
        if credentials is None:
            conn = self.__get_conn_as_admin()
        else:
            conn = psycopg2.connect(
                host=get_env_variable("POSTGRES_HOST"),
                database=get_env_variable("POSTGRES_DB_NAME"),
                user=credentials["username"],
                password=credentials["password"],
                port=get_env_variable("POSTGRES_PORT"),
            )
        return conn

    def close_conn(self, conn):
        if conn:
            conn.close()
        else:
            print("Connection is None, cannot close")