from flask import Config as FlaskConfig


class Config(FlaskConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///DataBase.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'fgefsfdeg3r23rf5g6h73g'

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = 'flaskforstudents@gmail.com'
    MAIL_PASSWORD = 'DANfed27'
    EMAIL_HOST_PASSWORD = 'galwcmeoyyzsgdtp'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    MAX_CONTENT_LENGTH = 1024 * 1024



