import os
import jwt
import datetime

fake_link = "http://localhost:5000/api/v1/auth/reset-password/verify" \
            "/Im5haWlmZ0BnbWFkZmFkc2ZzZGZzZGZpbC5jb21kIg.DSwpyw.xAS1IkwDjuPpA2ydCjcFgNHRAtE "
expired_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9" \
                ".eyJleHAiOjE1MTM3OTI5OTEsImlhdCI6MTUxMzYyMDE5MSwic3ViIjoxfQ" \
                ".7fO_hfHaFyp0IMH24Kl0s6StdnVJxdTGKi5dNQ1pr5U"

fake_token = "ldsjfkajdsfajsr95803495493sdtjiortue9005384058934sdfasdfasdf9874942079472"


def encode_token():
    print(os.environ.get("SECRET"))
    """
    Generating a token that'll expire in 3 milliseconds
    :return:token
    """
    try:
        payload = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(milliseconds=3),
            "iat": datetime.datetime.utcnow(),
            "sub": 1
        }
        return jwt.encode(
            payload,
            os.environ.get("SECRET"),
            algorithm="HS256"
        )
    except Exception as e:
        return e



correct_user = {
    "name": "Kilango Jumiya",
    "email": "naiifg@gmadfadsfsdfsdfil.comd",
    "password": "secreting"
}

invalid_email_user = {
    "name": "Kilango Jumiya",
    "email": "naiifg",
    "password": "secreting"
}
correct_user2 = {
    "name": "Junior Yusuph",
    "email": "yusuphjunior@gmail.com",
    "password": "secretsldkjfasd"
}
reset_email = "naiifg@gmadfadsfsdfsdfil.comd"
incorrect_reset_email = "naiifg@gmadfadsfsdfsdfil.comdfsd"
wrong_input_user = {
    "name": "Kilango Jumiya",
    "password": "secretfsadfasdfa"
}
empty_input_user = {
    "email": "",
    "password": ""
}
wrong_email_user = {
    "email": "juma@gmail.com",
    "password": "jfklasdfjjasdjfjaslkd"
}
wrong_password_user = {
    "email": "naiifg@gmadfadsfsdfsdfil.comd",
    "password": "jfklasdjkflasdf"
}
BASE_URL = "http://localhost:5000"
new_password = {
    "password": "123456789",
    "password_confirmation": "123456789"
}
new_password_wrong = {
    "password": "123e",
    "password_confirmation": "123"
}

new_password_empty_fields = {
    "password": "",
    "password_confirmation": ""
}

correct_event = {
    "name": "Coders Campusess",
    "address": "Magomeni, Dar es salaam",
    "start_date": "1/12/2019",
    "end_date": "2/8/2000",
    "description": "This isn't something you can miss",
    "price": "Free",
    "category": "Bootcamp",
    "user_id": 1,
    "category_id": 1
}

updated_correct_event = {
    "name": "Googly Fellas",
    "address": "Magomeni, Dar es salaam",
    "start_date": "1/12/2019",
    "end_date": "2/8/2000",
    "description": "This isn't something you can miss",
    "price": "Free",
    "category": "Bootcamp",
    "user_id": 1,
    "category_id": 1
}

updated_wrong_user_event = {
    "name": "Googly Fellas",
    "address": "Magomeni, Dar es salaam",
    "start_date": "1/12/2019",
    "end_date": "2/8/2000",
    "description": "This isn't something you can miss",
    "price": "Free",
    "category": "Bootcamp",
    "user_id": 2,
    "category_id": 1
}

missing_field_event = {
    "address": "Magomeni, Dar es salaam",
    "start_date": "1/12/2019",
    "end_date": "2/8/2000",
    "description": "This isn't something you can miss",
    "price": "Free",
    "category": "Bootcamp",
    "user_id": 1,
    "category_id": 1
}
