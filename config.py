import os


class configuration(object):
    DEBUG = True
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ENGINE_OPTIONS = {
        "max_overflow": 15,
        "pool_pre_ping": True,
        "pool_recycle": 60 * 60,
        "pool_size": 30,
    }
    SECURITY_PASSWORD_SALT = 'salt'
    SECURITY_PASSWORD_HASH = 'bcrypt'
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS")
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL")
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    RECAPTCHA_USE_SSL = os.environ.get('RECAPTCHA_USE_SSL')
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')
    RECAPTCHA_PARAMETERS = {'hl': 'ru'} # 'render': 'explicit'
    RECAPTCHA_DATA_ATTRS = {'theme':'white'}
