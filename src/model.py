from pydantic import BaseModel
from typing import List


class SentenceInput(BaseModel):
    sentence: str


class OutputModel(BaseModel):
    output: List[float]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str
