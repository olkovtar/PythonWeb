import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEVELOPMENT = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'test_secret_key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True


class DevConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    WTF_CSRF_ENABLED = True
    if os.getenv('DATABASE_URL'):
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://", 1)
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'site.db')


class TestConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test_site.db')


class ProdConfig(Config):
    WTF_CSRF_ENABLED = True
    if os.getenv('DATABASE_URL'):
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://", 1)
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'site.db')


config = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'default': DevConfig,
    'test': TestConfig,
}
