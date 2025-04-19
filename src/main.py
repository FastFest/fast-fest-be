import os

from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy import select
from starlette.requests import Request
from starlette.staticfiles import StaticFiles

from dto import QuestionRead, TicketInfoRead
from middleware.auth_middleware import AuthCheckMiddleware
from middleware.db_middleware import DBSessionMiddleware
from models import Question, Ticket, TicketInfo
from routes.auth import auth_router
from routes.mypage import mypage_router
from routes.qna import qna_router
from routes.ticket import ticket_router
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
app.include_router(qna_router, prefix="/qna")
app.include_router(ticket_router, prefix="/ticket")
app.include_router(mypage_router, prefix="/mypage")


@app.get("/")
async def home(request: Request):
    session = request.state.db_session
    result = session.execute(select(Question))
    questions = [QuestionRead.from_orm(q) for q in result.scalars().all()]
    sorted_questions = sorted(questions, key=lambda q: q.created_at, reverse=True)
    result = session.execute(select(TicketInfo))
    tickets = [TicketInfoRead.from_orm(t) for t in result.scalars().all()]
    sorted_tickets = sorted(tickets, key=lambda t: t.id, reverse=True)
    return templates.TemplateResponse("index.html",
            {"request": request, "questions": sorted_questions, "tickets": sorted_tickets})
