from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):
    login = StringField("Login: ", validators=[DataRequired(), Length(min=2, max=20)])
    psw = PasswordField("Password: ", validators=[DataRequired(), Length(min=4, max=20)])
    remember = BooleanField("Remember: ", default=False)
    submit = SubmitField("Enter")


class RegistrationForm(FlaskForm):
    login = StringField("Login: ", validators=[DataRequired(), Length(min=2, max=20)])
    psw1 = PasswordField("Password: ", validators=[DataRequired(), Length(min=4, max=20)])
    psw2 = PasswordField("Repeat Password: ", validators=[
        DataRequired(),
        EqualTo('psw1', message="Passwords dont match!"),
        Length(min=4, max=20)])
    email = StringField("Email: ", validators=[DataRequired(), Email(), Length(min=4, max=30)])
    submit = SubmitField("Register")


class ChangeEmailLoginForm(FlaskForm):
    login = StringField(
        "Login: ",
        validators=[DataRequired(), Length(min=2, max=20)],
    )
    email = StringField(
        "Email: ",
        validators=[DataRequired(), Email(), Length(min=4, max=30)],
    )
    submit = SubmitField("Enter")


class ChangePasswordForm(FlaskForm):
    old_psw = PasswordField("Old Password: ", validators=[DataRequired(), Length(min=4, max=20)])
    psw1 = PasswordField("Password: ", validators=[DataRequired(), Length(min=4, max=20)])
    psw2 = PasswordField("Repeat Password: ", validators=[
        DataRequired(),
        EqualTo('psw1', message="Passwords dont match!"),
        Length(min=4, max=20)])
    submit = SubmitField("Enter")

