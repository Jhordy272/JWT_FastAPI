from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.Auth_Service import AuthService
from app.services.User_Service import UserService
from app.db.Database_Connection_ORM import DatabaseConnectionORM
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT

router = APIRouter()

def get_session(session=Depends(DatabaseConnectionORM().get_session)) -> AuthService:
    return session

@router.get("")
def get_users(session: Session = Depends(get_session), auth: AuthJWT = Depends()):

    user_service = UserService(session)
    user_data = AuthService.validate_token(auth)
    print(user_data)

    users = user_service.get_users()
    if users:
        return [UserResponse.from_orm(user) for user in users]
    else:
        raise HTTPException(status_code=400, detail="Error getting users")
    
@router.get("/{id}")
def get_user_by_id(id: int, session: Session = Depends(get_session), auth: AuthJWT = Depends()):

    user_service = UserService(session)
    user_data = AuthService.validate_token(auth)
    print(user_data)

    user = user_service.get_user_by_id(id)
    if user:
        return UserResponse.from_orm(user)
    else:
        raise HTTPException(status_code=404, detail="User not found")
    
@router.get("/limited/")
def get_users_limited(page:int, items:int, session: Session = Depends(get_session), auth: AuthJWT = Depends()):

    user_service = UserService(session)
    user_data = AuthService.validate_token(auth)
    print(user_data)
    if page <= 0 or items <= 0:
        raise HTTPException(status_code=400, detail="Page and items must be positive integers")

    users = user_service.get_users_limited(page,items)
    if users:
        return [UserResponse.from_orm(user) for user in users]
    else:
        raise HTTPException(status_code=404, detail="No users found")

@router.post("")
def create_user(user: UserCreate, session: Session = Depends(get_session), auth: AuthJWT = Depends()):
    
    auth_service = AuthService(session)
    user_service = UserService(session)
    user_data = AuthService.validate_token(auth)
    print(user_data)
    if not auth_service.validate_user(user.username,user.password):
        password_encode = auth_service.get_password_hash(user.password)
        user_service.create_user(user.username, password_encode)
        raise HTTPException(status_code=201, detail="User created")
    else:
        raise HTTPException(status_code=400, detail="Error creating user")
    
@router.put("/{id}")
def update_user(id: int, user_update: UserUpdate, session: Session = Depends(get_session), auth: AuthJWT = Depends()):
    auth_service = AuthService(session)
    user_service = UserService(session)
    
    user_data = AuthService.validate_token(auth)
    print(user_data)

    user = user_service.get_user_by_id(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_update.username:
        user.username = user_update.username
    
    if user_update.password:
        user.password = auth_service.get_password_hash(user_update.password)

    user_service.update_user(user)
    raise HTTPException(status_code=200, detail="User edited successfully")


@router.delete("/{id}")
def delete_user_by_id(id: int, session: Session = Depends(get_session), auth: AuthJWT = Depends()):

    user_service = UserService(session)
    user_data = AuthService.validate_token(auth)
    print(user_data)

    user = user_service.get_user_by_id(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_service.delete_user(user)
    raise HTTPException(status_code=200, detail="User deleted successfully")