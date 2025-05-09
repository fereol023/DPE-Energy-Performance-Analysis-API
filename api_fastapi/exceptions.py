from fastapi import HTTPException, Request
from api_fastapi import validate_reader_identity
import asyncio


def exception_handler(if_error_status=500):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                raise HTTPException(
                    status_code=if_error_status,
                    detail=f"Error occurred: {e}"
                )
        return wrapper
    return decorator


def validate_reader_handler(func):
    """
    Decorator to validate the reader identity using a JWT token.
    The token should be passed in the request headers.
    """
    def wrapper(*args, **kwargs):
        print("IDENTITY CHECKING .....")
        request: Request = kwargs.get("request")
        if not request:
            raise HTTPException(
                status_code=400,
                detail="Request object is required"
            )

        token = request.headers.get("Authorization")
        if not token:
            raise HTTPException(
                status_code=401,
                detail="Authorization token is missing"
            )

        if not asyncio.run(validate_reader_identity(token)):
            raise HTTPException(
                status_code=403,
                detail="Identity not valid"
            )
        print("CHECKED !")
        return func(*args, **kwargs)
    return wrapper
