from flask_login import UserMixin


class UserLogin(UserMixin):
    def fromDB(self, id, db):
        user = db.query.where(db.id == id).limit(1)
        us = user[0]
        self.user = us
        return self

    def create(self, user):
        self.user = user
        return self

    def get_id(self):
        return self.user.id

    def get_login(self):
        return self.user.login

