from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from instance.config import env_config

db = SQLAlchemy()

from api.auth.views import auth
from api.events.views import events


def create_app(environment):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(env_config[environment])
    app.config.from_pyfile("config.py")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.register_blueprint(auth)
    app.register_blueprint(events)
    db.init_app(app)

    return app
