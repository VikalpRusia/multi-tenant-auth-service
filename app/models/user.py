from sqlalchemy import Column, String, JSON, Integer, BigInteger
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email: str = Column(String(20), unique=True, nullable=False)
    password: str = Column(String(20), nullable=False)
    profile: dict = Column(JSON, default={}, nullable=False)
    status: int = Column(Integer, default=0, nullable=False)
    settings: dict = Column(JSON, default={}, nullable=True)
    created_at: int = Column(BigInteger, nullable=True)
    updated_at: int = Column(BigInteger, nullable=True)
