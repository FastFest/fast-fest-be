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
