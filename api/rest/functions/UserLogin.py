from flask_login import UserMixin


class UserLogin(UserMixin):
    def __init__(self, user):
        self.user = user

    def get_id(self):
        return self.user.id

    def get_login(self):
        return self.user.login

    def get_user(self):
        return self.user

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



def get_user_from_db(db, id = None, login = None):
    if id:
        user_ar = db.query.where(db.id == id).limit(1)
    else:
        user_ar = db.query.where(db.login == login).limit(1)
    try:
        return user_ar[0]
    except IndexError as er:
        return None