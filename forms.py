from flask_wtf.file import FileField, FileAllowed
from flask_wtf import FlaskForm, RecaptchaField
from flask_login import current_user
from wtforms import Form, StringField, PasswordField, SubmitField, BooleanField, TextAreaField,SelectMultipleField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError




class PostForm(Form):
    title = StringField('Title')
    description = TextAreaField('description')


class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить')
    submit = SubmitField('Авторизоваться')
    recaptcha=RecaptchaField()


class UpdateProfile(FlaskForm):
    phone=StringField('Номер телефона', validators=[DataRequired(), Length(min=2, max=60)])
    picture=FileField('Обновить аватар', validators=[FileAllowed(['jpg', 'png'])])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Обновить профиль')

class RegisterForm(FlaskForm):
    login = StringField('Придумайте логин', validators=[DataRequired(), Length(min=2, max=40)])
    name = StringField('Имя', validators=[DataRequired(), Length(min=2, max=100)])
    surname = StringField('Фамилия', validators=[DataRequired(), Length(min=2, max=150)])
    patronymic = StringField('Отчество', validators=[DataRequired(), Length(min=2, max=255)])
    street = SelectField('Улица', choices=[('Украинская', 'Украинская')])
    house_number = SelectField('Номер дома', choices=[('50', '50')])
    apartment_number = StringField('Номер квартиры', validators=[DataRequired(), Length(min=1, max=20)])
    phone = StringField('Номер телефона', validators=[DataRequired(), Length(min=2, max=60)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=2, max=60)])
    confirm_password = PasswordField('Подтвердите пароль',
                                     validators=[DataRequired(), EqualTo('password')])
    recaptcha = RecaptchaField()



    submit = SubmitField('Создать')
