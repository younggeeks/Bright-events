import os

from flask import render_template, send_from_directory
from api import create_app

environment = os.getenv("ENV_SETTINGS")
app = create_app(environment)


@app.route("/")
def docs():
    return render_template("docs.html")


@app.route("/<path:path>")
def imagesServe(path):
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
    return send_from_directory(root, path)

@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

if __name__ == '__main__':
    app.run()
