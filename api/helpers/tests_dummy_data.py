fake_link = "http://localhost:5000/api/v1/auth/reset-password/verify" \
       "/Im5haWlmZ0BnbWFkZmFkc2ZzZGZzZGZpbC5jb21kIg.DSwpyw.xAS1IkwDjuPpA2ydCjcFgNHRAtE "
expired_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9" \
                ".eyJleHAiOjE1MTM3OTI5OTEsImlhdCI6MTUxMzYyMDE5MSwic3ViIjoxfQ" \
                ".7fO_hfHaFyp0IMH24Kl0s6StdnVJxdTGKi5dNQ1pr5U"

correct_user = {
    "name": "Kilango Jumiya",
    "email": "naiifg@gmadfadsfsdfsdfil.comd",
    "password": "secret"
}
correct_user2 = {
    "name": "Junior Yusuph",
    "email": "yusuphjunior@gmail.com",
    "password": "secret"
}
reset_email = "naiifg@gmadfadsfsdfsdfil.comd"
incorrect_reset_email = "naiifg@gmadfadsfsdfsdfil.comdfsd"
wrong_input_user = {
    "name": "Kilango Jumiya",
    "password": "secret"
}
empty_input_user = {
    "email": "",
    "password": ""
}
wrong_email_user = {
    "email": "juma@gmail.com",
    "password": "11234"
}
wrong_password_user = {
    "email": "naiifg@gmadfadsfsdfsdfil.comd",
    "password": "asfsadf"
}
BASE_URL = "http://localhost:5000"
new_password = {
    "password": "123",
    "password_confirmation": "123"
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
