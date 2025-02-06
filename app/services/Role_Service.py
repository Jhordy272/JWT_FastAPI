from app.db.models import Role
from app.db.models.Role import Rol

class RoleService:
    def __init__(self, session):
        self.session = session

    def get_role_by_id(self, id):
        return self.session.query(Rol).filter(Rol.id == id).first()

    def get_role_by_name(self, name):
        return self.session.query(Rol).filter(Rol.name == name).first()
    
    def get_roles(self):
        return self.session.query(Rol).all()
    
    def get_roles_limited(self, page: int = 1, items: int = 10):
        offset = (page - 1) * items
        return self.session.query(Rol).limit(items).offset(offset).all()
    
    def exists_role_by_id(self, id):
        rol = self.session.query(Rol).filter(Rol.id == id).first()
        return rol is not None
    
    def exists_role_by_name(self, name):
        rol = self.session.query(Rol).filter(Rol.name == name).first()
        return rol is not None
    
    def create_role(self, name):
        rol = Rol()
        rol.name = name
        self.session.add(rol)
        self.session.commit()
        return
    
    def update_role(self, role: Role):
        self.session.commit()
    
    def delete_role(self, role: Role):
        self.session.delete(role)
        self.session.commit()
    