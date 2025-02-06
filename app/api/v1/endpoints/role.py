from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends
from app.schemas.role import RoleCreate, RoleResponse, RoleUpdate
from app.services.Auth_Service import AuthService
from app.services.Role_Service import RoleService
from app.db.Database_Connection_ORM import DatabaseConnectionORM
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT

router = APIRouter()

def get_session(session=Depends(DatabaseConnectionORM().get_session)) -> AuthService:
    return session

@router.get("")
def get_roles(session: Session = Depends(get_session), auth: AuthJWT = Depends()):

    rol_service = RoleService(session)
    user_data = AuthService.validate_token(auth)
    print(user_data)

    roles = rol_service.get_roles()
    if roles:
        return [RoleResponse.from_orm(role) for role in roles]
    else:
        raise HTTPException(status_code=404, detail="No roles found")
    
@router.get("/{id}")
def get_role_by_id(id: int, session: Session = Depends(get_session), auth: AuthJWT = Depends()):

    role_service = RoleService(session)
    user_data = AuthService.validate_token(auth)
    print(user_data)

    user = role_service.get_role_by_id(id)
    if user:
        return RoleResponse.from_orm(user)
    else:
        raise HTTPException(status_code=404, detail="Role not found")
    
@router.get("/limited/")
def get_roles_limited(page:int, items:int, session: Session = Depends(get_session), auth: AuthJWT = Depends()):

    role_service = RoleService(session)
    user_data = AuthService.validate_token(auth)
    print(user_data)
    if page <= 0 or items <= 0:
        raise HTTPException(status_code=400, detail="Page and items must be positive integers")

    roles = role_service.get_roles_limited(page,items)
    if roles:
        return [RoleResponse.from_orm(role) for role in roles]
    else:
        raise HTTPException(status_code=404, detail="No roles found")
    
@router.post("")
def create_role(role: RoleCreate, session: Session = Depends(get_session), auth: AuthJWT = Depends()):
    
    role_service = RoleService(session)
    user_data = AuthService.validate_token(auth)
    print(user_data)
    if not role_service.exists_role_by_name(role.name):
        role_service.create_role(role.name)
        raise HTTPException(status_code=201, detail="Role created")
    else:
        raise HTTPException(status_code=400, detail="Error creating role")
    
@router.put("/{id}")
def update_user(id: int, role_update: RoleUpdate, session: Session = Depends(get_session), auth: AuthJWT = Depends()):
    auth_service = AuthService(session)
    role_service = RoleService(session)
    
    user_data = AuthService.validate_token(auth)
    print(user_data)

    role = role_service.get_role_by_id(id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    if role_update.name:
        role.name = role_update.name

    role_service.update_role(role)
    raise HTTPException(status_code=200, detail="Role edited successfully")

@router.delete("/{id}")
def delete_user_by_id(id: int, session: Session = Depends(get_session), auth: AuthJWT = Depends()):

    role_service = RoleService(session)
    user_data = AuthService.validate_token(auth)
    print(user_data)

    role = role_service.get_role_by_id(id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    role_service.delete_role(role)
    raise HTTPException(status_code=200, detail="Role deleted successfully")