from app.db.models import Role
from app.db.models.Role import Role

class RoleService:
    def __init__(self, session):
        self.session = session

    def get_role_by_id(self, id):
        return self.session.query(Role).filter(Role.id == id).first()

    def get_role_by_name(self, name):
        return self.session.query(Role).filter(Role.name == name).first()
    
    def get_roles(self):
        return self.session.query(Role).all()
    
    def get_roles_limited(self, page: int = 1, items: int = 10):
        offset = (page - 1) * items
        return self.session.query(Role).limit(items).offset(offset).all()
    
    def exists_role_by_id(self, id):
        rol = self.session.query(Role).filter(Role.id == id).first()
        return rol is not None
    
    def exists_role_by_name(self, name):
        role = self.session.query(Role).filter(Role.name == name).first()
        return role is not None
    
    def create_role(self, name):
        role = Role()
        role.name = name
        self.session.add(role)
        self.session.commit()
        return
    
    def update_role(self, role: Role):
        self.session.commit()
    
    def delete_role(self, role: Role):
        self.session.delete(role)
        self.session.commit()
    