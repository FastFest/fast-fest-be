from fastapi import APIRouter
from sqlalchemy import select
from starlette.requests import Request

from dto import TicketRead, TicketInfoRead
from models import Ticket, TicketInfo
from template import templates

mypage_router = APIRouter()


@mypage_router.get("")
async def mypage_get(request: Request):
    user = request.state.user
    session = request.state.db_session
    result = session.execute(select(Ticket).where(Ticket.user_id == user.id))
    tickets = [TicketRead.from_orm(t) for t in result.scalars().all()]
    result = session.execute(select(TicketInfo).where(TicketInfo.id.in_([t.ticket_id for t in tickets])))
    ticket_info = [TicketInfoRead.from_orm(t) for t in result.scalars().all()]
    print(len(ticket_info), len(tickets))
    for info in ticket_info:
        for ticket in tickets:
            if ticket.ticket_id == info.id:
                ticket.price = info.price
                ticket.title = info.title
    return templates.TemplateResponse("mypage.html", {"request": request, "user": user, "tickets": tickets})

