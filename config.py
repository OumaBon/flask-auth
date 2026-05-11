import os 
from dotenv import load_dotenv
from datetime import timedelta
load_dotenv()


Base_Dir = os.path.abspath(os.path.dirname(__file__))



class Config:
    SECRET_KEY = os.getenv("SECRET_KEY") or \
    "Iwantolovethenatureofcodingandsucksups"
    DEBUG = True
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', None)
    
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") or \
    "somethingIdontwanttoshare"
    JWT_ACCESS_TOKEN_EXPIRES = os.getenv("TOKEN_EXPIRES") or \
    timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_ACCESS_COOKIE_NAME = "access_token_cookie"
    JWT_REFRESH_COOKIE_NAME = "refresh_token_cookie"
    JWT_COOKIE_HTTPONLY = True
    JWT_COOKIE_SECURE = False 
    JWT_COOKIE_SAMESITE = "Lax"
    JWT_COOKIE_CSRF_PROTECT = True


    @staticmethod
    def init_app(self):
        pass


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URI') or \
    "sqlite:///" + os.path.join(Base_Dir, "dev-data.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS = True 
    REDIS_BLACKLIST_DB = 0


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URI") or \
    "sqlite:///" + os.path.join(Base_Dir, "test-data.sqlite")


config = {
    "default": DevelopmentConfig,
    "development": DevelopmentConfig,
    "testing": TestingConfig
}