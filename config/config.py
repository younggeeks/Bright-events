class Config:
    Testing = False


class Development(Config):
    Testing = False
    BASE_URL = "http://localhost:5000"


class Production(Config):
    Testing = False
    BASE_URL = "https://bright-event.herokuapp.com"


class Testing(Config):
    Testing = True
    BASE_URL = "http://localhost:5000"


environments = {
    "testing": Testing,
    "development": Development,
    "production": Production
}
