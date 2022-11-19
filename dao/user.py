from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(User).all()

    def create(self, user_d):
        ent = User(**user_d)
        self.session.add(ent)
        self.session.commit()
        return ent

    def delete(self, username):
        user = self.get_user_by_username(username)
        self.session.delete(user)
        self.session.commit()

    def update(self, data, username):
        self.session.query(User).filter(User.username == username).update(data)
        self.session.commit()

    def get_user_by_username(self, username):
        return self.session.query(User).filter(User.username == username).first()
