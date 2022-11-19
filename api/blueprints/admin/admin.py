from flask import Blueprint, render_template, make_response, request, flash, redirect, url_for
from flask_login import login_required, current_user, login_user
from sqlalchemy.exc import IntegrityError

from rest.base import login_manager, app
from rest.functions.UserLogin import UserLogin
from rest.functions.images import image_is_png
from rest.models.db_classes import Users, db

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, Users)


@admin.route('/profile')
@login_required
def profile():
    return render_template('admin/profile.html', user=current_user.user)


@admin.route('/userava')
@login_required
def userava():
    img = current_user.get_user_image(app)
    if not img:
        return ""

    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h


@admin.route('/upload', methods=["POST", "GET"])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file = image_is_png(file, app)
            if file:
                res = update_user(image=file)
                if res:
                    flash("Success!", "success")
                    return redirect(url_for('.profile'))
                flash("Error while updating user image!", "error")
            else:
                flash("Error while reading image file!", "error")
        else:
            flash("No new file for update!", "error")

    return redirect(url_for('.profile'))


def update_user(login=None, psw=None, email=None, image=None):
    user = current_user.user
    if login:
        user.login = login
    if psw:
        user.password = psw
    if email:
        user.email = email
    if image:
        user.image = image
    try:
        db.session.commit()
        login_user.user = user
    except Exception as ex:
        db.session.rollback()
        if type(ex) == IntegrityError:
            flash(f'User with this login or email already exists !!!', category='error')
            return False
        flash(f'Error with database {ex} !!!', category='error')
        return False
    return True
