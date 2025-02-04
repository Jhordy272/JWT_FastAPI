from app.db.models.User import User
from app.db.Database_Connection_ORM import DatabaseConnectionORM

class UserService:
    def __init__(self, session):
        self.session = session

    def get_user_by_username(self, username):
        return self.session.query(User).filter(User.username == username).first()
    
    def create_user(self, username, password):
        user = self.session.query(User).filter(User.username == username).first()
        if user is None:
            user = User()
            user.username = username
            user.password = password
            self.session.add(user)
            self.session.commit()
        return