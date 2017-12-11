import jwt
import os

from api import db
import datetime

events_subscriptions = db.Table("subscriptions",
                                db.Column("id", db.Integer, db.ForeignKey("users.id")),
                                db.Column("id", db.Integer, db.ForeignKey("events.id")))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(165), unique=True)
    name = db.Column(db.String(250))
    password = db.Column(db.String(250))
    email = db.Column(db.String(80), unique=True)
    events = db.relationship("Event", back_populates="user")
    # rsvps = db.relationship("Event", secondary=events_subscriptions, back_populates="guests")
    __tablename__ = "users"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def encode_token(self):
        """
        Using User ID To generate Token
        :return:string
        """
        try:
            payload = {
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=2),
                "iat": datetime.datetime.utcnow(),
                "sub": self.id
            }
            return jwt.encode(
                payload,
                os.getenv("SECRET"),
                algorithm="HS256"
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_token(auth_token):
        """Using Secret Key To Decode auth_token"""
        try:
            payload = jwt.decode(auth_token, os.getenv("SECRET"))
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            return "Token Expired , Please Login Again"
        except jwt.InvalidTokenError:
            return "Invalid Toke , Please Login again"


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    events = db.relationship("Event", back_populates="category")
    __tablename__ = "categories"


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(200))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates="events")
    category = db.relationship("Category", back_populates="events")
    # guests = db.relationship("User", secondary=events_subscriptions, back_populates="rsvps")

    __tablename__ = "events"
