from typing import Optional

from pydantic import BaseModel

class UserSchemaAdd(BaseModel):
    login: str
    password: str
    role: str


class UserSchemaResponse(BaseModel):
    id: int
    login: str
    role: str



class Token(BaseModel):
    access_token: str
    token_type: str
