from flask import Blueprint, render_template, make_response, request, flash, redirect, url_for
from flask_login import login_required, current_user, login_user, logout_user
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from api.rest.base import login_manager, app
from api.rest.functions.UserLogin import UserLogin
from api.rest.functions.forms import RegistrationForm, ChangeEmailLoginForm, ChangePasswordForm
from api.rest.functions.images import image_is_png
from api.rest.models.db_classes import Users, db

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, Users)


@admin.route('/profile')
@login_required
def profile():
    return render_template('admin/profile.html', user=current_user.user)


@admin.route('/edit_user_log_email',  methods=["POST", "GET"])
@login_required
def edit_user_log_email():
    form = ChangeEmailLoginForm()
    if form.validate_on_submit():
        if update_user(login=form.login.data, email=form.email.data):
            flash("Success!", "success")
            return redirect(url_for('.profile'))
    return render_template('admin/edit_user_log_email.html', form=form, user=current_user.user)


@admin.route('/edit_user_psw',  methods=["POST", "GET"])
@login_required
def edit_user_psw():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if check_password_hash(current_user.user.password, form.old_psw.data):
            if update_user(psw=generate_password_hash(form.psw1.data)):
                flash("Success!", "success")
                return redirect(url_for('.profile'))
        flash('Incorrect old password!!!', category='error')
    return render_template('admin/edit_user_psw.html', form=form, user=current_user.user)


@admin.route('/userava')
@login_required
def userava():
    img = current_user.get_user_image(app)
    if not img:
        return ""

    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h


@admin.route('/upload_image', methods=["POST", "GET"])
@login_required
def upload_image():
    if request.method == 'POST':
        if request.files['image']:
            file = image_is_png(request.files['image'], app)
            if file:
                if update_user(image=file):
                    flash("Success!", "success")
                    return redirect(url_for('.profile'))
                flash("Error while updating user image!", "error")
            else:
                flash("Error while reading image file!", "error")
        else:
            flash("No new file for update!", "error")

    return redirect(url_for('.profile'))


@admin.route('/sign_out')
def sign_out():
    logout_user()
    flash('Logout successfully!', category='success')
    return redirect('/')


@admin.errorhandler(404)
def page_not_found():
    return render_template("404.html")


@admin.errorhandler(401)
def no_access():
    return render_template("401.html")


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


