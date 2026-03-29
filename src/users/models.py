from sqlalchemy import Column, Integer, String, Boolean

from src.utils.db import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hash_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
