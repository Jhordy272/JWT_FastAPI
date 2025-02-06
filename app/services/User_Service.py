from app.db.models.User import User

class UserService:
    def __init__(self, session):
        self.session = session

    def get_user_by_username(self, username):
        return self.session.query(User).filter(User.username == username).first()
    
    def get_user_by_id(self, id):
        return self.session.query(User).filter(User.id == id).first()
    
    def get_users(self):
        return self.session.query(User).all()
    
    def get_users_limited(self, page: int = 1, items: int = 10):
        offset = (page - 1) * items
        return self.session.query(User).limit(items).offset(offset).all()

    def create_user(self, username, password):
        user = self.session.query(User).filter(User.username == username).first()
        if user is None:
            user = User()
            user.username = username
            user.password = password
            self.session.add(user)
            self.session.commit()
        return
    
    def update_user(self, user: User):
        self.session.commit()
    
    def delete_user(self, user : User):
        self.session.delete(user)
        self.session.commit()