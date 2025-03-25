from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import declarative_base

from enums import UserRole

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer)
    email = Column(String, unique=True)
    password = Column(String)
    name = Column(String)
    nickname = Column(String)
    role = Column(Enum(UserRole))