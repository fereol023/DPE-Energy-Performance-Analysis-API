import jwt
import datetime
from api_utils.commons import get_env_variable
import asyncio


def create_reader_jwt_token():

    username = get_env_variable("POSTGRES_READER_USERNAME") # exceptions deja gérées
    password = get_env_variable("POSTGRES_READER_PASSWORD")
    token_expiration_hours = get_env_variable("JWT_TOKEN_EXPIRATION_HOURS", default=1)

    payload = {
        "username": username,
        "password": password,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=token_expiration_hours)
    }
    
    # secret key for signing the token
    secret_key = get_env_variable("API_SECRET_KEY")
    
    # generate the JWT token
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token


def decode_jwt_token(token):
    secret_key = get_env_variable("API_SECRET_KEY")
    try:
        # decode the JWT token
        decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise ValueError("Sorry, token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")


def validate_reader_identity_simple(token):
    try:
        decoded_token = decode_jwt_token(token)
        # prendre les cles username et password du payload
        # et verifier si elles matchent avec celles de l'environnement de l'api
        username = decoded_token.get("username")
        password = decoded_token.get("password")
        if (username == get_env_variable("POSTGRES_READER_USERNAME")) and (password == get_env_variable("POSTGRES_READER_PASSWORD")):
            return True
        return False
    except ValueError as e:
        raise e
    except Exception as e:
        raise ValueError(f"An error occurred while validating the token: {str(e)}")
    

async def validate_reader_identity(token):
    try:
        decoded_token = await asyncio.to_thread(decode_jwt_token, token)
        # prendre les cles username et password du payload
        # et verifier si elles matchent avec celles de l'environnement de l'api
        username = decoded_token.get("username")
        password = decoded_token.get("password")
        if (username == get_env_variable("POSTGRES_READER_USERNAME")) and (password == get_env_variable("POSTGRES_READER_PASSWORD")):
            return True
        return False
    except ValueError as e:
        raise e
    except Exception as e:
        raise ValueError(f"An error occurred while validating the token: {str(e)}")