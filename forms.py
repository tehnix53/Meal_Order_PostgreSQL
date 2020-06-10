from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, DataRequired, Length


class LoginForm(FlaskForm):
    mail = StringField("Электропочта:", validators=[InputRequired(), Length(min=5)])
    password = PasswordField("Пароль:", validators=[DataRequired(), Length(min=5)])


class OrderForm(FlaskForm):
    address = StringField("Адрес", validators=[InputRequired()])
    phone = StringField("Телефон", validators=[InputRequired()])
