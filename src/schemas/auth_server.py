from pydantic import BaseModel
from typing import Union


class ServerCreate(BaseModel):
    name: str
    port: str
    ip: str
    user: str
    password: str

class ServerModel(ServerCreate):
    id: int

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    login: str
    password: str

class UserModel(UserCreate):
    id: int

    class Config:
        from_attributes = True