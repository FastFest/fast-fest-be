from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from enums import UserRole


class UserCreate(BaseModel):
    student_id: int
    email: str
    password: str
    name: str
    nickname: str
    role: UserRole = UserRole.USER


class UserLogin(BaseModel):
    email: str
    password: str


class UserRead(BaseModel):
    id: int
    student_id: int
    email: str
    name: str
    nickname: str
    role: UserRole = UserRole.USER

    class Config:
        orm_mode = True
        from_attributes = True


class QuestionCreate(BaseModel):
    writer_id: Optional[int] = None
    title: str
    content: str

class QuestionRead(BaseModel):
    id: int
    writer_id: int
    title: str
    content: str
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True

class AnswerCreate(BaseModel):
    question_id: int
    writer_id: Optional[int] = None
    content: str

class AnswerRead(BaseModel):
    id: int
    question_id: int
    writer_id: int
    content: str
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True


class TicketInfoRead(BaseModel):
    id: int
    title: str
    quantity: int
    left_quantity: int
    price: int

    class Config:
        orm_mode = True
        from_attributes = True

class TicketInfoCreate(BaseModel):
    title: str
    quantity: int
    left_quantity: Optional[int] = None
    price: int


class TicketRead(BaseModel):
    id: int
    ticket_id: int
    tocket_number: int
    user_id: int
    pay: bool

    class Config:
        orm_mode = True
        from_attributes = True


class TicketCreate(BaseModel):
    ticket_id: int
    ticket_number: int
    user_id: int
    pay: bool = False
