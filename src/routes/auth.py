from fastapi import APIRouter
from sqlalchemy import select
from starlette import status
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse

from models import User
from template import templates
from dto import UserRead, UserRole, UserCreate, UserLogin
from util.token import access_token_gen

auth_router = APIRouter(
    tags=["Auth"],
)


@auth_router.get("/signup")
def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@auth_router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@auth_router.post("/signup")
def signup(request: Request, response: Response, user_in: UserCreate):
    session = request.state.db_session
    new_user = User(**user_in.dict())
    session.add(new_user)
    session.commit()
    response.status_code = status.HTTP_201_CREATED
    return response


@auth_router.post("/login")
def login(request: Request, response: Response, user_in: UserLogin):
    session = request.state.db_session
    result = session.execute(select(User).where(User.email == user_in.email))
    user = result.scalars().one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    if user_in.password != user.password:
        raise HTTPException(status_code=401, detail="Incorrect password")
    response.set_cookie("access_token", access_token_gen(user.id))  # ✅ 쿠키 설정 예시
    response.status_code = status.HTTP_200_OK
    return response
