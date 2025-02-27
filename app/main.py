from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException
from contextlib import asynccontextmanager

from app.db.Database_Connection_ORM import DatabaseConnectionORM
from app.security import auth
from app.api.v1.endpoints import role, user

db = DatabaseConnectionORM()
Base = db.get_base()
engine = db.get_engine()
Base.metadata.create_all(engine)
session = db.get_session()

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.openapi_schema = app.openapi()
    
    if app.openapi_schema and 'components' not in app.openapi_schema:
        app.openapi_schema['components'] = {}

    app.openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    app.openapi_schema["security"] = [{"BearerAuth": []}]
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(auth.router, prefix="/auth")
app.include_router(user.router, prefix="/user")
app.include_router(role.router, prefix="/role")

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )