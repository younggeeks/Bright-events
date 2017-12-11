import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from api import create_app, db

app = create_app(os.getenv("ENV_SETTINGS"))

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()
