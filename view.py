from app import app, limiter
from forms import LoginForm, PostForm, UpdateProfile, RegisterForm
from flask import Flask, render_template, redirect, url_for, request, abort, flash
from sqlalchemy import desc
from models import *
from flask_login import login_user, login_required, logout_user, current_user


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/contacts')
def contacts_func():
    contacts_data=contacts.query.all()
    return render_template('contacts.html', contacts_data=contacts_data)


@app.route('/news')
def news_func():
    page=request.args.get('page')
    if page and page.isdigit():
        page=int(page)
    else:
        page=1
    news_data_host_post=news.query.order_by(desc(news.created_at))
    pages=news_data_host_post.paginate(page=page, per_page=5)
    return render_template('news.html', news_data_host_post=news_data_host_post, pages=pages)


@app.route('/news/create_news', methods=['POST', 'GET'])
@login_required
def create_news():
    if request.method == 'POST':
        title=request.form['title']
        description=request.form['description']

        try:
            news_post=news(title=title, description=description)
            db.session.add(news_post)
            db.session.commit()
        except Exception:
            print('Error')

        return redirect(url_for('news_func'))
    else:
        form=PostForm()
        return render_template('create_news.html', form=form)


@app.route('/news/<slug>')
def news_detail(slug):
    news_detail_data_host_post=news.query.filter(news.slug == slug).first()
    return render_template('news_detail.html', news_detail_data_host_post=news_detail_data_host_post)


@app.route('/services', methods=['GET'])
def services_func():
    services_data=services.query.all()
    return render_template('services.html', services_data=services_data)


@app.route('/information')
def information_func():
    return render_template('information.html')


@app.route('/government')
def government_func():
    government_data=government.query.all()
    return render_template('government.html', government_data=government_data)


@app.route('/documents')
def documents_func():
    return render_template('documents.html')


@app.route('/house-information')
def house_information_func():
    return render_template('house-information.html')
