import os

from flask import render_template

from api import create_app

environment = os.getenv("ENV_SETTINGS")
app = create_app(environment)


@app.route("/")
def docs():
    return render_template("docs.html")


if __name__ == '__main__':
    app.run()
