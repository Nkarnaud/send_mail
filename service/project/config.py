import os


def getenv(name, default=None, typehandler=str):
    if name in os.environ:
        return typehandler(os.environ[name])
    elif default is None:
        raise RuntimeError('OS Envrionment `{}` is required.'.format(name))
    else:
        return default


class BaseConfig:
    """Base configuration"""
    TESTING = False
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    VR_SERVICE_URL = os.environ.get('VR_SERVICE_URL')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SECURITY_SALT = os.environ.get('SECURITY_SALT')
    TOKEN_EXPIRATION_DAYS = 5
    TOKEN_EXPIRATION_SECONDS = 0
    DEFAULT_ITERATION_TIMEOUT = \
        getenv('DEFAULT_ITERATION_TIMEOUT', 10800.0, float)


class DevelopmentConfig(BaseConfig):
    """
    Development environment configuration
    """
    TESTING = False
    DEBUG_TB_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class ProductionConfig(BaseConfig):
    """
    Production environment configurations
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class TestingConfig(BaseConfig):
    """
    Development environment configuration
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
