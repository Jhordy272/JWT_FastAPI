from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.db.Database_Connection_ORM import DatabaseConnectionORM

db_connection = DatabaseConnectionORM()
Base = db_connection.get_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    password = Column(String)
    role = Column(Integer, ForeignKey('role.id'))
    role_obj = relationship("Role", backref="users", foreign_keys=[role])

    def __repr__(self):
        return f"<User(id='{self.id}', username='{self.username}', password='{self.password}, role={self.role_obj}')>"