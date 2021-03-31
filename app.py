from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from modules.check_distance import CheckDistanceJob
from datetime import datetime
import os, re

app = Flask(__name__)

app.config.update(
    SQLALCHEMY_DATABASE_URI = "sqlite:///fitbit.db",
    SQLALCHEMY_TRACK_MODIFICATIONS = False,
    SECRET_KEY = os.getenv('SECRET_KEY'),
    SCHEDULER_API_ENABLED = True
)

db = SQLAlchemy(app)
def check_distance_job():
    return CheckDistanceJob().call()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    client_id = db.Column(db.String, nullable=False)
    client_secret = db.Column(db.String, nullable=False)
    target_distance = db.Column(db.Integer, nullable=True)
    access_token = db.Column(db.Text, nullable=True)
    refresh_token = db.Column(db.String, nullable=True)
    pixela_user_name = db.Column(db.String, nullable=False, default='')
    pixela_user_token = db.Column(db.Text, nullable=False, default='')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())

    def __init__(self, name, client_id, client_secret, target_distance=None, access_token=None, refresh_token=None, pixela_user_name=None, pixela_user_token=None):
        self.name = name
        self.client_id = client_id
        self.client_secret = client_secret
        self.target_distance = target_distance
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.pixela_user_name = pixela_user_name
        self.pixela_user_token = pixela_user_token
