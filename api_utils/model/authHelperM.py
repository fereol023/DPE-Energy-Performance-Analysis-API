from pydantic import BaseModel, EmailStr, validator, Field
from email_validator import validate_email, EmailNotValidError

# by using Pydantic's built-in EmailStr
class UserWithEmail(BaseModel):
    name: str
    email: EmailStr 

# based on this : https://github.com/JoshData/python-email-validator