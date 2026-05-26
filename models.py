from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class BloodPressure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    systolic = db.Column(db.Integer, nullable=False)  # Систолическое давление
    diastolic = db.Column(db.Integer, nullable=False)  # Диастолическое давление
    mean_pressure = db.Column(db.Float, nullable=False)  # Среднее артериальное давление
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<BloodPressure {self.systolic}/{self.diastolic} at {self.date}>'

    @staticmethod
    def calculate_mean_pressure(systolic, diastolic):
        """Расчёт среднего артериального давления по формуле"""
        return diastolic + (systolic - diastolic) / 3
