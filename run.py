import os

from api import create_app

environment = os.getenv("ENV_SETTINGS")
app = create_app(environment)

if __name__ == '__main__':
    app.run()
