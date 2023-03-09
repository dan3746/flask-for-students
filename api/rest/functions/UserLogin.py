from flask import url_for
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

    def get_user_image(self, app):
        img = None
        if self.user.image:
            img = self.user.image
        else:
            try:
                with app.open_resource(app.blueprints['profile'].static_folder + f'/images/base_user_image.png', "rb") as f:
                    img = f.read()
            except FileNotFoundError as e:
                print(f"File was not found: {e}")
        return img
