import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from instance.config import env_config

db = SQLAlchemy()


def create_app(environment):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(env_config[environment])
    app.config.from_pyfile("config.py")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    print(os.getenv("POSTGRES_DATABASE_URI"))
    return app
