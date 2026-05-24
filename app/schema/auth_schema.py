from pydantic import BaseModel, Field, EmailStr, field_validator
import re

class LoginRequest(BaseModel):
    email: EmailStr
    password: str 

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    email: str
    user_id: int