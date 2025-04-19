from urllib import response

from fastapi import APIRouter
from sqlalchemy import select, update
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from dto import TicketInfoRead, TicketInfoCreate, TicketDetailRead, UserRead
from enums import UserRole
from models import Ticket, TicketInfo, User
from template import templates

ticket_router = APIRouter(
    tags=["Ticket"],
)


@ticket_router.get("")
async def get_all_tickets(request: Request):
    user = request.state.user
    session = request.state.db_session
    result = session.execute(select(TicketInfo))
    tickets = [TicketInfoRead.from_orm(t) for t in result.scalars().all()]
    sorted_tickets = sorted(tickets, key=lambda t: t.id, reverse=True)
    html_file = "ticket.html"
    if user.role == UserRole.ADMIN:
        html_file = "ticket_admin.html"
    return templates.TemplateResponse(html_file, {"request": request, "tickets": sorted_tickets})


@ticket_router.get("/new")
async def new_ticket_form(request: Request):
    return templates.TemplateResponse("ticket_create.html", {"request": request})


@ticket_router.post("")
async def create_ticket(request: Request, response: Response, ticket_info_in: TicketInfoCreate):
    # if request.state.user.role != UserRole.ADMIN:
    #     response.status_code = status.HTTP_403_FORBIDDEN
    #     return response
    session = request.state.db_session
    ticket_info_in.left_quantity = ticket_info_in.quantity
    new_ticket_info = TicketInfo(**ticket_info_in.dict())
    session.add(new_ticket_info)
    session.commit()
    response.status_code = status.HTTP_201_CREATED
    return response

@ticket_router.get("/{ticket_id}/applicants")
async def ticket_applicants(request: Request, ticket_id: int):
    session = request.state.db_session
    result = session.execute(select(TicketInfo).where(TicketInfo.id == ticket_id))
    ticket_info = TicketInfoRead.from_orm(result.scalars().one_or_none())
    ticket_title = ticket_info.title
    result = session.execute(select(Ticket).where(Ticket.ticket_id == ticket_id))
    tickets = [TicketDetailRead.from_orm(t) for t in result.scalars().all()]
    result = session.execute(select(User).where(User.id.in_([t.user_id for t in tickets])))
    users = [UserRead.from_orm(u) for u in result.scalars().all()]
    for t in tickets:
        for u in users:
            if u.id == t.user_id:
                t.name = u.name
                t.student_id = u.student_id
    return templates.TemplateResponse("ticket_detail.html", {"request": request, "ticket_title": ticket_title, "applicants": tickets})

@ticket_router.put("/{ticket_id}/confirm")
async def confirm_ticket(request: Request, response: Response, ticket_id: int):
    session = request.state.db_session
    session.execute(update(Ticket).where(Ticket.ticket_id == ticket_id).values(pay=True))
    session.commit()
    response.status_code = status.HTTP_200_OK
    return response



@ticket_router.post("/{ticket_id}")
async def apply_ticket(request: Request, response: Response, ticket_id: int):
    # if request.state.user.role == UserRole.ADMIN:
    #     response.status_code = status.HTTP_403_FORBIDDEN
    #     return response
    user_id = request.state.user.id
    session = request.state.db_session
    ticket = (session.execute(select(TicketInfo).where(TicketInfo.id == ticket_id))).scalar_one_or_none()
    if ticket.left_quantity == 0:
        response.status = status.HTTP_400_BAD_REQUEST
        return response
    ticket_history = (session.execute(select(Ticket).where(Ticket.id == ticket_id and Ticket.user_id == user_id))).scalar_one_or_none()
    if ticket_history:
        response.status_code = status.HTTP_403_FORBIDDEN
        return response
    session.execute(update(TicketInfo).where(TicketInfo.id == ticket_id).values(left_quantity=ticket.left_quantity - 1))
    session.add(Ticket(ticket_id=ticket_id, ticket_number=ticket.quantity - ticket.left_quantity, user_id=user_id, pay= False))
    session.commit()
    response.status_code = status.HTTP_201_CREATED
    return response
