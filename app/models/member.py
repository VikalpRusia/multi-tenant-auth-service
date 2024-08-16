from sqlalchemy import Column, Integer, ForeignKey, JSON, BigInteger
from sqlalchemy.orm import declarative_base

from .role import Role
from .organization import Organization
from .user import User

Base = declarative_base()


class Member(Base):
    __tablename__ = "members"
    id = Column(Integer, primary_key=True, autoincrement=True)
    org_id = Column(
        Integer, ForeignKey(Organization.id, ondelete="CASCADE"), nullable=False
    )
    user_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"), nullable=False)
    role_id = Column(Integer, ForeignKey(Role.id, ondelete="CASCADE"), nullable=False)
    status = Column(Integer, default=0, nullable=False)
    settings = Column(JSON, default={}, nullable=True)
    created_at = Column(BigInteger, nullable=True)
    updated_at = Column(BigInteger, nullable=True)

    def __setitem__(self, key, value):
        self.__setattr__(key, value)
