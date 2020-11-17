from app import app, limiter
import secrets, os, datetime
from PIL import Image
from forms import LoginForm, PostForm, UpdateProfile, RegisterForm
from flask import Flask, render_template, redirect, url_for, request, abort, flash
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import desc
from werkzeug.security import generate_password_hash, check_password_hash
from security.token import generate_confirmation_token, confirm_token
from security.email_sender import send_email
from security.token import confirm_token
from decorators import check_confirmed
from models import *


@app.route('/lk/index')
@login_required
@check_confirmed
def user_panel_index():
    page=request.args.get('page')
    if page and page.isdigit():
        page=int(page)
    else:
        page=1
    news_data_host_post=news.query.order_by(desc(news.created_at))
    pages=news_data_host_post.paginate(page=page, per_page=5)
    return render_template('UserPanel/index.html', news_data_host_post=news_data_host_post, pages=pages)


def save_picture(form_picture):
    random_hex=secrets.token_hex(8)
    _, f_ext=os.path.splitext(form_picture.filename)
    picture_file=random_hex + f_ext
    picture_path=os.path.join(app.root_path, 'static/avatars', picture_file)

    output_size=(125, 125)
    i=Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_file


@app.route('/lk/profile', methods=['POST', 'GET'])
@login_required
@check_confirmed
def user_panel_profile():
    form=UpdateProfile()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file=save_picture(form.picture.data)  # save_picture is the function created above
            current_user.image_file=picture_file

        if form.email.data != current_user.email:
            user_check=user.query.filter_by(email=form.email.data).first()
            if user_check:
                flash('Такой email уже используется в системе! Введите другой email')
                return redirect(url_for('user_panel_profile'))

        current_user.phone=form.phone.data
        current_user.email=form.email.data
        db.session.commit()
        flash('Ваш профиль был обновлен', 'success')
        return redirect(url_for('user_panel_profile'))

    elif request.method == 'GET':
        form.phone.data=current_user.phone
        form.email.data=current_user.email

    image_file=url_for('static', filename='avatars/' + current_user.image_file)
    return render_template('UserPanel/profile.html', image_file=image_file, form=form, current_user=current_user)


@app.route('/lk/appeal', methods=['POST', 'GET'])
@login_required
@check_confirmed
def user_panel_appeal():
    if request.method == 'POST':
        theme=request.form.get('theme')
        text_appeal=request.form.get('text-appeal')
        try:
            new_appeal=appeal(theme=theme, description=text_appeal, user_id=current_user.id)
            db.session.add(new_appeal)
            db.session.commit()
        except Exception:
            print('Ошибка')
        return redirect(url_for('user_panel_history_appeal'))
    else:
        form=PostForm()
        return render_template('UserPanel/appeal.html', form=form)


@app.route('/lk/history_appeal?id=<uid>')
@login_required
@check_confirmed
def user_panel_history_appeal_uid(uid):
    user_appeal_data_uid=appeal.query.filter(appeal.uid == uid).first()
    return render_template('UserPanel/appeal_uid.html', user_appeal_data_uid=user_appeal_data_uid)


@app.route('/lk/history_appeal')
@login_required
@check_confirmed
def user_panel_history_appeal():
    page=request.args.get('page')

    if page and page.isdigit():
        page=int(page)
    else:
        page=1

    user_appeal_data=appeal.query.filter(current_user.id == appeal.user_id).order_by(desc(appeal.created_at))
    user_appeal_pages=user_appeal_data.paginate(page=page, per_page=10)
    return render_template('UserPanel/history_appeal.html', user_appeal_data=user_appeal_data,
                           user_appeal_pages=user_appeal_pages)


@app.route('/lk/payments/?id=<uid>')
@login_required
@check_confirmed
def user_panel_history_payments_uid(uid):
    user_appeal_data_uid=appeal.query.filter(appeal.uid == uid).first()
    return render_template('UserPanel/payments_uid.html', user_appeal_data_uid=user_appeal_data_uid)


@app.route('/lk/payments')
@login_required
@check_confirmed
def user_panel_history_payments():
    page=request.args.get('page')

    if page and page.isdigit():
        page=int(page)
    else:
        page=1

    user_appeal_data=appeal.query.filter(current_user.id == appeal.user_id).order_by(desc(appeal.created_at))
    user_appeal_pages=user_appeal_data.paginate(page=page, per_page=10)
    return render_template('UserPanel/payments.html', user_appeal_data=user_appeal_data,
                           user_appeal_pages=user_appeal_pages)
