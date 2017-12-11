import os

from api import create_app
from api.auth.views import auth

environment = os.getenv("ENV_SETTINGS")
app = create_app(environment)


app.register_blueprint(auth)

if __name__ == '__main__':
    app.run()