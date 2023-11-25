from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    login = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, index=True, nullable=False, default=None)


class Server(Base):
    __tablename__ = "servers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True)
    port = Column(String)
    ip = Column(String)
    user = Column(String)
    password = Column(String)
    owner_id = Column(Integer, index=True)
