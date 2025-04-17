from fastapi import APIRouter
from sqlalchemy import select
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from dto import QuestionRead, AnswerRead, QuestionCreate, AnswerCreate
from models import Question, Answer
from template import templates

qna_router = APIRouter(
    tags=["Qna"],
)


@qna_router.get("")
async def get_qna(request: Request):
    session = request.state.db_session
    result = session.execute(select(Question))
    questions = [QuestionRead.from_orm(q) for q in result.scalars().all()]
    sorted_questions = sorted(questions, key=lambda q: q.created_at, reverse=True)
    return templates.TemplateResponse("qna.html",
                                      {"request": request, "questions": sorted_questions})


@qna_router.get("/write")
async def get_qna(request: Request):
    return templates.TemplateResponse("qna_write.html", {"request": request})


@qna_router.post("/question")
async def get_qna(request: Request, response: Response, question_in: QuestionCreate):
    question_in.writer_id = request.state.user.id
    session = request.state.db_session
    new_question = Question(**question_in.dict())
    session.add(new_question)
    session.commit()
    response.status_code = status.HTTP_201_CREATED
    return response


@qna_router.post("/answer")
async def get_qna(request: Request, response: Response, answer_in: AnswerCreate):
    answer_in.writer_id = request.state.user.id
    session = request.state.db_session
    new_answer = Answer(**answer_in.dict())
    session.add(new_answer)
    session.commit()
    response.status_code = status.HTTP_201_CREATED
    return response


@qna_router.get("/{question_id}")
async def get_qna(request: Request, question_id: int):
    session = request.state.db_session
    result = session.execute(select(Question).where(Question.id == question_id))
    question = QuestionRead.from_orm(result.scalars().one_or_none())
    result = session.execute(select(Answer).where(Answer.question_id == question_id))
    answers = [AnswerRead.from_orm(a) for a in result.scalars().all()]
    return templates.TemplateResponse("qna_detail.html", {"request": request, "question": question, "answer": answers})
