from flask import Flask, render_template, redirect, url_for, request,abort
from flask_sqlalchemy import SQLAlchemy
from flask_security import SQLAlchemyUserDatastore, Security
from sqlalchemy import desc
from config import configuration
from forms import PostForm
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.config.from_object(configuration)

limiter = Limiter(
    app,
    key_func=get_remote_address,

)

db = SQLAlchemy(app)
from models import *

# TODO
# migrate = Migrate(app, db)
# manager = Manager(app)
# manager.add_command('db', MigrateCommand)

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return user.query.get(user_id)


admin = Admin(app)
admin.add_view(ModelView(news, db.session))


