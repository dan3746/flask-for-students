from flask import render_template, request, redirect
from flask_login import current_user

from api.rest.base import app
from api.rest.models.db_classes import Statistic, db
from api.blueprints.admin.admin import admin
from api.blueprints.menu.menu import menu
from api.rest.views.user import user_is_logged

MAX_CONTENT_LENGTH = 1024 * 1024

app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(menu, url_prefix='')


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


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
