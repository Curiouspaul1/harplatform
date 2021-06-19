import os
from dotenv import load_dotenv
from harperdb import HarperDB

load_dotenv()

class Config:
    SECRET_KEY=os.getenv('SECRET_KEY')


class DevelopmentConfig(Config):
    DATABASE_URL=os.getenv("DB_URL")
    DATABASE_KEY=os.getenv("DB_KEY")
    DATABASE_USERNAME=os.getenv("DB_USERNAME")
    DATABASE_PASSWORD=os.getenv("DB_PASSWORD")
    DB = HarperDB(
        username=DATABASE_USERNAME,
        password=DATABASE_PASSWORD,
        url=DATABASE_URL
    )
    FLASK_ENV=os.getenv('FLASK_ENV')
    DEBUG=os.getenv('DEBUG')


class ProductionConfig(Config):
    pass


class TestingConfig(Config):
    pass


config={
    "development":DevelopmentConfig,
    "production":ProductionConfig,
    "testing":TestingConfig,
    "default":DevelopmentConfig
}
