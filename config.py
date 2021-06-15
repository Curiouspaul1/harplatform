import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY=os.getenv('SECRET_KEY')


class DevelopmentConfig(Config):
    DATABASE_URL=os.getenv("DB_URL")
    DATABASE_KEY=os.getenv("DB_KEY")
    DATABASE_USERNAME=os.getenv("DB_USERNAME")
    DATABASE_PASSWORD=os.getenv("DB_PASSWORD")


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