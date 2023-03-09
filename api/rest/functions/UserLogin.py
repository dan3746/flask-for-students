from flask import url_for
from flask_login import UserMixin


class UserLogin(UserMixin):
    def fromDB(self, db, id = None, login = None):
        user = db.query.where((db.id == id) | (db.login == login)).limit(1)
        try:
            self.user = user[0]
            return self
        except IndexError as er:
            print(er)
            return None

    def create(self, user):
        self.user = user
        return self

    def get_user(self):
        return self.user

    def get_id(self):
        return self.user.id

    def get_login(self):
        return self.user.login

    def get_psw(self):
        return self.user.password

    def get_user_image(self, app):
        img = None
        if self.user.image:
            img = self.user.image
        else:
            try:
                with app.open_resource(app.blueprints['admin'].static_folder + f'/images/base_user_image.png', "rb") as f:
                    img = f.read()
            except FileNotFoundError as e:
                print(f"File was not found: {e}")
        return img
