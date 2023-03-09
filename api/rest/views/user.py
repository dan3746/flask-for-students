from flask_login import current_user


def user_is_logged():
    return current_user if current_user.is_authenticated else None
