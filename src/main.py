import os

from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.requests import Request
from starlette.staticfiles import StaticFiles

from middleware.auth_middleware import AuthCheckMiddleware
from middleware.db_middleware import DBSessionMiddleware
from routes.auth import auth_router
from template import templates

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "view", "static")

# ✅ 정적 파일 mount
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# app.mount("/static", StaticFiles(directory="src/view/static"), name="static")
app.add_middleware(AuthCheckMiddleware)
app.add_middleware(DBSessionMiddleware)


app.include_router(auth_router, prefix="/auth")


@app.get("/")
async def home(request: Request):
    print("라우터")
    return templates.TemplateResponse("index.html", {"request": request, "name": "정민"})

