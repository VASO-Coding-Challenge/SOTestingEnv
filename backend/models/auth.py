from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    name: str


class LoginData(BaseModel):
    name: str  # Using `name` here to be consistent with the login parameter
    password: str
