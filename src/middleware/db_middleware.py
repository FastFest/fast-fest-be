from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from database import SessionLocal


class DBSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        db = SessionLocal()
        request.state.db_session = db
        try:
            response = await call_next(request)
            return response
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()
