from app import app, limiter
from forms import LoginForm, PostForm, UpdateProfile, RegisterForm
from flask import Flask, render_template, redirect, url_for, request, abort, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from security.token import generate_confirmation_token, confirm_token
from security.email_sender import send_email
from security.token import confirm_token
from models import *


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('user_panel_login') + '?next=' + request.url)

    return response


@app.route('/lk/login', methods=['POST', 'GET'])
def user_panel_login():
    if current_user.is_authenticated:
        return redirect(url_for('user_panel_index'))

    form=LoginForm()

    if form.validate_on_submit():
        user_data=user.query.filter_by(login=form.login.data).first()

        if not user.is_active:
            flash('Пользователь заблокирован', 'danger')
            # TODO

        if user_data and check_password_hash(user_data.password, form.password.data):
            login_user(user_data, remember=form.remember.data)
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('user_panel_index'))
        else:
            flash('Неверный логин или пароль', 'danger')

    return render_template('UserPanel/login2.html', form=form)


@app.route('/lk/register', methods=['POST', 'GET'])
def user_panel_register():
    if current_user.is_authenticated:
        return redirect(url_for('user_panel_index'))

    form=RegisterForm()

    if form.validate_on_submit():
        user_check_login=user.query.filter_by(login=form.login.data).first()
        if user_check_login:
            flash('Такой логин уже используется в системе! Введите другой логин')
            return redirect(url_for('user_panel_register'))

        user_check_email=user.query.filter_by(email=form.email.data).first()
        if user_check_email:
            flash('Такой email уже используется в системе! Введите другой email')
            return redirect(url_for('user_panel_register'))

        hash_passwd=generate_password_hash(form.password.data)

        new_user=user(login=form.login.data, name=form.name.data, surname=form.surname.data,
                      patronymic=form.patronymic.data,
                      street=form.street.data, house_number=form.house_number.data,
                      apartment_number=form.apartment_number.data,phone=form.phone.data, email=form.email.data,
                      password=hash_passwd)
        db.session.add(new_user)
        db.session.commit()

        token=generate_confirmation_token(form.email.data)
        confirm_url=url_for('confirm_email', token=token, _external=True)
        html=render_template('email/email_confirm.html', confirm_url=confirm_url, user_email=user.email)
        subject="Пожалуйста, подтвердите свою электронную почту"
        send_email('ah.bideev@mail.ru', subject, html)
        login_user(new_user)

        flash('Ваш аккаунт был создан. Подтвердите Email', 'success')

        return redirect(url_for('uncofirm'))

    return render_template('UserPanel/register.html', form=form)


@app.route('/lk/resend')
@limiter.limit("2 per second")
def resend_confirm():
    token=generate_confirmation_token(current_user.email)
    confirm_url=url_for('confirm_email', token=token, _external=True)
    html=render_template('email/email_confirm.html', confirm_url=confirm_url, user_email=current_user.email)
    subject="Пожалуйста, подтвердите свою электронную почту"
    send_email(current_user.email, subject, html)
    flash('Мы отправили новое письмо с подтверждением', 'success')
    return redirect(url_for('uncofirm'))


@app.route('/lk/confirm/<token>')
def confirm_email(token):
    try:
        email=confirm_token(token)
    except:
        flash('Ссылка для подтверждения недействительна или срок ее действия истек', 'danger')
    user_check_email=user.query.filter_by(email=email).first_or_404()
    if user_check_email.confirmed:
        flash('Аккаунт уже подтвержден. Пожалуйста, авторизуйтесь', 'success')
    else:
        user_check_email.confirmed=True
        user_check_email.confirmed_on=datetime.now()

        db.session.add(user_check_email)
        db.session.commit()
        flash('Вы подтвердили свою учетную запись. Спасибо!', 'success')
    return redirect(url_for('user_panel_index'))


@app.route('/lk/unconfirmed')
def uncofirm():
    try:
        if current_user.confirmed:
            return redirect(url_for('user_panel_index'))
        return render_template('UserPanel/uncofirm.html')
    except Exception:
        return "Ошибка"


@app.route('/lk/password_change', methods=['POST'])
@login_required
def password_change():
    pass


@app.route('/lk/logout', methods=['POST', 'GET'])
def user_panel_logout():
    logout_user()
    # flash("Вы вышли из системы")
    return redirect(url_for('index'))


@app.route('/lk/forgot')
def user_panel_forgot():
    return render_template('UserPanel/forgot.html')


@app.route('/lk/reset_password')
def user_panel_reset_passwd():
    return render_template('UserPanel/reset_password.html')
