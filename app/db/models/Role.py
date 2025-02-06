from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.db.Database_Connection_ORM import DatabaseConnectionORM

db_connection = DatabaseConnectionORM()
Base = db_connection.get_base()

class Rol(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    def __repr__(self):
        return f"<User(id='{self.id}', name='{self.name}')>"