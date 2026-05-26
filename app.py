from flask import Flask
from models import db, BloodPressure
import os
basedir = os.path.abspath(os.path.dirname(__file__))

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "data", "pressure_data.db")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Инициализация базы данных
    db.init_app(app)

    # Создание таблиц при первом запуске
    with app.app_context():
        db.create_all()

    return app

app = create_app()

# Импортируем маршруты после создания приложения
from routes import *

if __name__ == '__main__':
    # Создаём директорию для данных, если её нет
    os.makedirs('data', exist_ok=True)
    app.run(debug=True)

