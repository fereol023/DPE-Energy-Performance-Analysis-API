from fastapi import HTTPException


def my_exception_handler(if_error_status=500):
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
