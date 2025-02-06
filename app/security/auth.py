from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends
from app.schemas.user import UserCreate
from app.services.Auth_Service import AuthService
from app.services.User_Service import UserService
from app.db.Database_Connection_ORM import DatabaseConnectionORM
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT

router = APIRouter()

def get_session(session=Depends(DatabaseConnectionORM().get_session)) -> AuthService:
    return session

@router.post("/login")
def login(user: UserCreate, session: Session = Depends(get_session)):
    auth_service = AuthService(session)
    if auth_service.validate_user(user.username,user.password):
        access_token = auth_service.create_access_token(data={"sub": user.username})
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
@router.post("/register")
def register(user: UserCreate, session: Session = Depends(get_session), auth: AuthJWT = Depends()):
    
    auth_service = AuthService(session)
    user_service = UserService(session)
    user_data = AuthService.validate_token(auth)
    print(user_data)
    if not auth_service.validate_user(user.username,user.password):
        password_encode = auth_service.get_password_hash(user.password)
        user_service.create_user(user.username, password_encode)
        raise HTTPException(status_code=201, detail="User registered")
    else:
        raise HTTPException(status_code=400, detail="Error registering user")