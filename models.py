from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from zoneinfo import ZoneInfo

db = SQLAlchemy()


class PressureRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    systolic = db.Column(db.Integer, nullable=False)     # систолическое
    diastolic = db.Column(db.Integer, nullable=False)    # диастолическое
    pulse = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(ZoneInfo("Europe/Moscow")))

