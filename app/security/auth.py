from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends
from app.services.Auth_Service import AuthService
from app.services.User_Service import UserService
from app.db.Database_Connection_ORM import DatabaseConnectionORM
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT

router = APIRouter()

def get_session(session=Depends(DatabaseConnectionORM().get_session)) -> AuthService:
    return session

@router.post("/login")
def login(username: str, password: str, session: Session = Depends(get_session)):
    auth_service = AuthService(session)
    if auth_service.validate_user(username,password):
        access_token = auth_service.create_access_token(data={"sub": username})
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
@router.post("/register")
def register(username: str, password: str, session: Session = Depends(get_session), auth: AuthJWT = Depends()):
    
    auth_service = AuthService(session)
    user_service = UserService(session)
    user_data = AuthService.validate_token(auth)
    print(user_data)
    if not auth_service.validate_user(username,password):
        password_encode = auth_service.get_password_hash(password)
        user_service.create_user(username, password_encode)
        raise HTTPException(status_code=201, detail="Usuario creado")
    else:
        raise HTTPException(status_code=400, detail="Error en la creación del usuario")