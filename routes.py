from flask import render_template, request, redirect, url_for, flash
from app import app, db
from models import BloodPressure
from datetime import datetime, timedelta

@app.route('/')
def index():
    """Главная страница с последней записью"""
    latest_pressure = BloodPressure.query.order_by(BloodPressure.date.desc()).first()
    return render_template('index.html', pressure=latest_pressure)

@app.route('/add', methods=['GET', 'POST'])
def add_pressure():
    """Добавление новых показаний давления"""
    if request.method == 'POST':
        try:
            systolic = int(request.form['systolic'])
            diastolic = int(request.form['diastolic'])

            # Проверка корректности данных
            if not (50 <= systolic <= 250) or not (30 <= diastolic <= 150):
                flash('Некорректные значения давления. Проверьте введённые данные.', 'error')
                return render_template('add_pressure.html')

            # Расчёт среднего давления
            mean_pressure = BloodPressure.calculate_mean_pressure(systolic, diastolic)

            # Создание новой записи
            new_pressure = BloodPressure(
                systolic=systolic,
                diastolic=diastolic,
                mean_pressure=mean_pressure
            )

            db.session.add(new_pressure)
            db.session.commit()

            flash('Показания давления успешно сохранены!', 'success')
            return redirect(url_for('index'))

        except ValueError:
            flash('Пожалуйста, введите корректные числовые значения.', 'error')

    return render_template('add_pressure.html')

@app.route('/statistics')
def statistics():
    """Страница со статистикой"""
    today = datetime.utcnow().date()

    # Статистика за неделю (последние 7 дней)
    week_ago = today - timedelta(days=7)
    week_data = BloodPressure.query.filter(BloodPressure.date >= week_ago).all()
    week_stats = calculate_statistics(week_data)

    # Статистика за месяц (последние 30 дней)
    month_ago = today - timedelta(days=30)
    month_data = BloodPressure.query.filter(BloodPressure.date >= month_ago).all()
    month_stats = calculate_statistics(month_data)

    # Статистика за год (последние 365 дней)
    year_ago = today - timedelta(days=365)
    year_data = BloodPressure.query.filter(BloodPressure.date >= year_ago).all()
    year_stats = calculate_statistics(year_data)

    # Общая статистика (все данные)
    all_data = BloodPressure.query.all()
    all_stats = calculate_statistics(all_data)

    return render_template(
        'statistics.html',
        week_stats=week_stats,
        month_stats=month_stats,
        year_stats=year_stats,
        all_stats=all_stats
    )

def calculate_statistics(data):
    """Расчёт статистики для набора данных"""
    if not data:
        return {
            'count': 0,
            'avg_systolic': 0,
            'avg_diastolic': 0,
            'avg_mean': 0,
            'max_systolic': None,
            'min_systolic': None,
            'max_diastolic': None,
            'min_diastolic': None,
            'max_mean': None,
            'min_mean': None
        }

    systolics = [p.systolic for p in data]
    diastolics = [p.diastolic for p in data]
    means = [p.mean_pressure for p in data]

    return {
        'count': len(data),
        'avg_systolic': sum(systolics) / len(systolics),
        'avg_diastolic': sum(diastolics) / len(diastolics),
        'avg_mean': sum(means) / len(means),
        'max_systolic': max(systolics),
        'min_systolic': min(systolics),
        'max_diastolic': max(diastolics),
        'min_diastolic': min(diastolics),
        'max_mean': max(means),
        'min_mean': min(means)
    }
