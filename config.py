import os 
from dotenv import load_dotenv

load_dotenv()


Base_Dir = os.path.abspath(os.path.dirname(__file__))



class Config:
    SECRET_KEY = os.getenv("SECRET_KEY") or \
    "Iwantolovethenatureofcodingandsucksups"
    DEBUG = True

    @staticmethod
    def init_app(self):
        pass


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URI') or \
    "sqlite:///" + os.path.join(Base_Dir, "dev-data.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS = True 


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URI") or \
    "sqlite:///" + os.path.join(Base_Dir, "test-data.sqlite")


config = {
    "default": DevelopmentConfig,
    "development": DevelopmentConfig,
    "testing": TestingConfig
}