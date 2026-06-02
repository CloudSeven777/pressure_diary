from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class PressureRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    systolic = db.Column(db.Integer, nullable=False)     # верхнее
    diastolic = db.Column(db.Integer, nullable=False)    # нижнее
    pulse = db.Column(db.Integer, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
