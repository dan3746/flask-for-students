from flask import render_template, request, redirect, flash, url_for, make_response
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

from api.rest.base import login_manager, app
from api.rest.functions.UserLogin import UserLogin
from api.rest.functions.forms import LoginForm, RegistrationForm
from api.rest.functions.images import image_is_png
from api.rest.models.db_classes import Users, Statistic, db
from api.blueprints.admin.admin import admin
from api.blueprints.menu.menu import menu

MAX_CONTENT_LENGTH = 1024 * 1024

app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(menu, url_prefix='')


def user_is_logged():
    return current_user.user if current_user.is_authenticated else None


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


@app.errorhandler(404)
def pageNotFound():
    return render_template("404.html")


@app.errorhandler(401)
def noAccess():
    return render_template("401.html")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
