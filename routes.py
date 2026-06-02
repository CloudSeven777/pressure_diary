from flask import render_template, request, redirect
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

