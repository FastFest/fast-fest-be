from sqlalchemy import Column, Integer, String, Enum, DateTime, func, Boolean
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


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    writer_id = Column(Integer)
    title = Column(String)
    content = Column(String)
    created_at = Column(DateTime, server_default=func.now())


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True)
    writer_id = Column(Integer)
    question_id = Column(Integer)
    content = Column(String)
    created_at = Column(DateTime, server_default=func.now())


class TicketInfo(Base):
    __tablename__ = "ticket_info"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    quantity = Column(Integer)
    left_quantity = Column(Integer)
    price = Column(Integer)


class Ticket(Base):
    __tablename__ = "ticket_mapping"
    id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer)
    ticket_number = Column(Integer)
    user_id = Column(Integer)
    pay = Column(Boolean)
