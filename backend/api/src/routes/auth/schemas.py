from datetime import timedelta
from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenWithExpiresAt(Token):
    expires: timedelta


class TokenData(BaseModel):
    username: Optional[str] = None


class SignInRequest(BaseModel):
    username: str
    password: str
