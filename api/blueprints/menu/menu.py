from sqlite3 import IntegrityError

from flask import Blueprint, render_template, request, flash, redirect, url_for, render_template_string
from flask_login import current_user, login_user
from werkzeug.security import check_password_hash, generate_password_hash

from api.rest.functions.UserLogin import UserLogin
from api.rest.functions.forms import LoginForm, RegistrationForm
from api.rest.models.db_classes import Statistic, Users, db

menu = Blueprint('menu', __name__, template_folder='templates', static_folder='static')


def user_is_logged():
    return current_user.user if current_user.is_authenticated else None


@menu.route('/')
def index():
    return render_template("menu/index.html", user=user_is_logged())


@menu.route('/about')
def about():
    return render_template("menu/about.html", user=user_is_logged())


@menu.route('/records')
def records():
    statistics = Statistic.query.order_by(Statistic.date).all()
    return render_template("menu/records.html", statistics=statistics, user=user_is_logged())


@menu.route('/contact', methods=['POST', "GET"])
def contact():
    if request.method == "POST":
        print(request.form)
        name = request.form['username']
        email = request.form['email']
        message = request.form['message']
        print(name + ' ---- ' + email + ' ---- ' + message)
        if len(message) > 2:
            flash('Message successfully sent!', category='success')
        else:
            flash('Error!', category='error')
    return render_template("menu/contact.html", user=user_is_logged())


@menu.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.profile'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.where(Users.login == form.login.data).limit(1)
        try:
            user = user[0]
        except IndexError as er:
            user = None
        if user and check_password_hash(user.password, form.psw.data):
            user_login = UserLogin().create(user)
            login_user(user_login, remember=form.remember.data)
            flash('Success!', category='success')
            return redirect(url_for('admin.profile'))
        flash('Error! Account not found!', category='error')
    return render_template("menu/login.html", form=form, user=user_is_logged())


@menu.route('/registration', methods=["POST", "GET"])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        login = form.login.data
        password = form.psw1.data
        email = form.email.data
        info = Users(login=login, password=generate_password_hash(password), email=email)
        try:
            db.session.add(info)
            db.session.commit()
            login_user(UserLogin().create(info))
        except Exception as ex:
            db.session.rollback()
            if type(ex) == IntegrityError:
                flash(f'User with this login or email already exists !!!', category='error')
                return render_template('menu/registration.html', user=user_is_logged())
            flash(f'Error with database {ex} !!!', category='error')
            return render_template('menu/registration.html', user=user_is_logged())
        flash('Your account has been successfully registered!', category='success')
        return redirect(url_for('admin.profile'))
    return render_template('menu/registration.html', form=form, user=user_is_logged())


@menu.app_errorhandler(404)
def page_not_found(err):
    return render_template("menu/404.html")


@menu.app_errorhandler(401)
def no_access(err):
    return render_template("menu/401.html")