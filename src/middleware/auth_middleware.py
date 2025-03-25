from fastapi import Request
from sqlalchemy import select
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse

from models import User
from util.token import jwt_decoder


class AuthCheckMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        if request.url.path.startswith("/auth/") or request.url.path.startswith("/static/"):
            response = await call_next(request)
            return response

        access_token = request.cookies.get('access_token')
        if not access_token:
            print("No access token")
            return JSONResponse(content={"message": "Unauthorized"}, status_code=401)

        try:
            user_id = jwt_decoder(access_token)
            session = request.state.db_session
            result = session.execute(select(User).where(User.id == user_id))
            user = result.scalars().one_or_none()
            if not user:
                raise Exception("User not found")
            request.state.user = user
        except Exception as e:
            print(e)
            return JSONResponse(content={"message": "Unauthorized"}, status_code=401)
        return await call_next(request)