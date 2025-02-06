from fastapi import HTTPException
from fastapi_jwt_auth import AuthJWT
from datetime import datetime, timedelta
from passlib.context import CryptContext
import os
from pydantic import BaseSettings
from app.db.models.User import User
from dotenv import load_dotenv

from app.services.User_Service import UserService

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__default_rounds=12)

load_dotenv()

class Settings(BaseSettings):
    AUTHJWT_SECRET_KEY: str = os.getenv("SECRET")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    # print(f"AUTHJWT_SECRET_KEY {AUTHJWT_SECRET_KEY}")
    # print(f"ALGORITHM {ALGORITHM}")
    # print(f"ACCESS_TOKEN_EXPIRE_MINUTES {ACCESS_TOKEN_EXPIRE_MINUTES}")

@AuthJWT.load_config
def get_config():
    return Settings()

class AuthService:
    def __init__(self, session):
        self.session = session

    def validate_user(self, username, password):
        try:
            userService = UserService(self.session)
            usuario = userService.get_user_by_username(username)
            if usuario is not None:
                return self.verify_password(password, usuario.password)
            else:
                return False
        except Exception as e:
            print(F"Error {e}")
            return False

    def create_access_token(self, data: dict) -> str:
        encoded_jwt = AuthJWT().create_access_token(subject=data["sub"])
        return encoded_jwt
    
    def validate_token(auth: AuthJWT) -> dict:
        auth.jwt_required()
        return auth.get_jwt_subject()

    def get_password_hash(self, password: str):
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)