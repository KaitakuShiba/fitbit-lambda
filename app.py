from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from modules.check_distance import CheckDistanceJob
from flask_apscheduler import APScheduler
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

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

@app.route("/", methods=["GET"])
def hello():
    return 'hello'

@scheduler.task('interval', id='check_distance_job', seconds=10_800, misfire_grace_time=900)
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
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())

    def __init__(self, name, client_id, client_secret, target_distance=None, access_token=None, refresh_token=None):
        self.name = name
        self.client_id = client_id
        self.client_secret = client_secret
        self.target_distance = target_distance
        self.access_token = access_token
        self.refresh_token = refresh_token
