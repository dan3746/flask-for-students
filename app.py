from flask import render_template, request, redirect, flash, url_for, make_response
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

from rest.base import login_manager, app
from rest.functions.UserLogin import UserLogin
from rest.functions.forms import LoginForm, RegistrationForm
from rest.functions.images import image_is_png
from rest.models.db_classes import Users, Statistic, db
from api.blueprints.admin.admin import admin
from api.blueprints.main_page.main_page import main_page

MAX_CONTENT_LENGTH = 1024 * 1024

app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(main_page, url_prefix='')


def user_is_logged():
    return current_user.user if current_user.is_authenticated else None


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, Users)


@app.route('/add_record', methods=['POST'])
def add_record():
    if request.method == "POST":
        user_id = request.form['user_id']
        game = request.form['game']
        win_loss = request.form['win_loss']
        winning_stat = request.form['winning_stat']
        date = request.form['date']
        stat = Statistic(user_id=user_id, game=game, win_loss=win_loss, winning_stat=winning_stat, date=date)
        try:
            db.session.add(stat)
            db.session.commit()
            return redirect('/')
        except Exception as ex:
            return "Error during saving progress in db: " + ex
    else:
        return render_template("add_record.html", user=user_is_logged())


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user.user)


@app.route('/userava')
@login_required
def userava():
    img = current_user.get_user_image(app)
    if not img:
        return ""

    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h


@app.route('/upload', methods=["POST", "GET"])
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
                    return redirect(url_for('profile'))
                flash("Error while updating user image!" "error")
            else:
                flash("Error while reading image file!" "error")
        else:
            flash("No new file for update!" "error")

    return redirect(url_for('profile'))


@app.errorhandler(404)
def pageNotFound():
    return render_template("404.html")


@app.errorhandler(401)
def noAccess():
    return render_template("401.html")


@app.route('/durak')
def durak():
    return render_template("durak.html")


@app.route('/minesweeper')
def minesweeper():
    return render_template("minesweeper.html")


@app.route('/poker')
def poker():
    return render_template("poker.html")


@app.route('/tic_tac_toe')
def tic_tac_toe():
    return render_template("tic-tac-toe.html")


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


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
