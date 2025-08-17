import os
import logging
import psycopg2
from enum import Enum


def get_env_variable(var_name, default_value=None, compulsory=False, cast_to_type=None):
    """
    Get an environment variable.
    Returns default_value if not set and value is not compulsory.
    Returns default_value if not set and value is compulsory, but logs a warning.
    Raises ValueError if compulsory and not set, without default_value.
    :param var_name: Name of the environment variable.
    :param default_value: Default value to return if the variable is not set.
    :param compulsory: If True, raises an error if the variable is not set and no default_value is provided.
    :param cast_to_type: Optional type to cast the value to (e.g., int, float, str).
    :return: The value of the environment variable or the default_value.
    :raises ValueError: If the variable is compulsory and not set without a default_value. 
    """
    value = os.getenv(var_name)
    if not value:
        if compulsory:
            if not default_value:
                raise ValueError(f"Environment variable {var_name} is not set and is compulsory.")
            else:
                logging.warning(f"Environment variable {var_name} is not set, using default value: {default_value}")
                value = default_value
        else:
            logging.warning(f"Environment variable {var_name} is not set, and is not compulsory, default value is : {default_value}")

    try:
        return cast_to_type(value) if cast_to_type is not None else value
    except ValueError as e:
        raise ValueError(f"Cannot cast environment variable {var_name} to {cast_to_type}: {e}")


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