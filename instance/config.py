import os


class Config:
    DEBUG = False
    SECRET = os.getenv("SECRET")
    SQLALCHEMY_DATABASE_URI = os.getenv('POSTGRES_DATABASE_URI')


class DevelopmentConfig(Config):
    DEBUG = True
    FRONTEND_URL = "http://localhost:3000"


class ProductionConfig(Config):
    DEBUG = False
    FRONTEND_URL = "https://bright-events-jwt.herokuapp.com"

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('POSTGRES_TEST_DATABASE_URI')


env_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    "production": ProductionConfig
}
