import os

from api import create_app
from api.auth.views import auth
from api.events.views import events

environment = os.getenv("ENV_SETTINGS")
app = create_app(environment)


app.register_blueprint(auth)
app.register_blueprint(events)

if __name__ == '__main__':
    app.run()