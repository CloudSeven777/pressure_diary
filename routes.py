from flask import render_template, request, redirect
from datetime import datetime, timedelta

from app import app
from models import db, PressureRecord


@app.route('/')
def index():
    records = PressureRecord.query.order_by(
        PressureRecord.created_at.desc()
    ).all()

    return render_template('index.html', records=records)


@app.route('/add', methods=['GET', 'POST'])
def add_pressure():

    if request.method == 'POST':

        systolic = request.form.get('systolic')
        diastolic = request.form.get('diastolic')
        pulse = request.form.get('pulse')

        new_record = PressureRecord(
            systolic=systolic,
            diastolic=diastolic,
            pulse=pulse
        )

        db.session.add(new_record)
        db.session.commit()

        return redirect('/')

    return render_template('add_pressure.html')



@app.route('/statistics')
def statistics():

    now = datetime.now()

    week_date = now - timedelta(days=7)
    month_date = now - timedelta(days=30)
    year_date = now - timedelta(days=365)

    week_records = PressureRecord.query.filter(
        PressureRecord.created_at >= week_date
    ).all()

    month_records = PressureRecord.query.filter(
        PressureRecord.created_at >= month_date
    ).all()

    year_records = PressureRecord.query.filter(
        PressureRecord.created_at >= year_date
    ).all()

    all_records = PressureRecord.query.all()

    def calc(records):
        if not records:
            return None

        return {
            "avg_sys": round(sum(r.systolic for r in records) / len(records), 1),
            "avg_dia": round(sum(r.diastolic for r in records) / len(records), 1),

            "max_sys": max(r.systolic for r in records),
            "max_dia": max(r.diastolic for r in records),

            "min_sys": min(r.systolic for r in records),
            "min_dia": min(r.diastolic for r in records),
        }

    stats = {
        "week": calc(week_records),
        "month": calc(month_records),
        "year": calc(year_records),
        "all": calc(all_records)
    }

    return render_template(
        'statistics.html',
        stats=stats
    )