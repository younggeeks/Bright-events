from flask import Flask

app = Flask(__name__)

app.config["SECRET_KEY"] = "KSDJFKLSAJDF9023753U0E-534425450440-385253475759253752598348579534"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite"

if __name__ == '__main__':
    app.run(debug=True)