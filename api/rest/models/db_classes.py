from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

from rest.base import app

db = SQLAlchemy(app)


class Statistic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('statistic.user_id'), nullable=False)
    game = db.Column(db.String(50), nullable=False)
    win_loss = db.Column(db.String(50), nullable=False)
    winning_stat = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Stat %r>' % self.id


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    image = db.Column(db.LargeBinary, nullable=True, default=None)
