import json
from flask import Flask, request, jsonify
import sqlite3
import datetime
from flask_cors import CORS
from flask_restful import Resource, Api, marshal_with, fields
from sqlalchemy import *
from flask_sqlalchemy import SQLAlchemy
import os
from functools import wraps
import jwt
import string
import random
import time
from time import sleep
import math
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd


app = Flask(__name__)
api = Api(app)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'data.db')
app.config['SECRET_KEY'] = 'secretkey'
regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
db = SQLAlchemy(app)

# decorator for token verification


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(
                public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated


class Measurement(db.Model):
    __tablename__ = 'measurements'
    id = db.Column(db.Integer, primary_key=True)
    degrees = db.Column(db.Float(precision=2))
    humidity = db.Column(db.Float(precision=2))
    date = db.Column(db.String)
    time = db.Column(db.String)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id'))


measurement_fields = {
    'id': fields.Integer,
    'degrees': fields.Float,
    'humidity': fields.Float,
    'date': fields.String,
    'time': fields.String,
    'sensor_id': fields.Integer,
}


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String, unique=True)
    username = db.Column(db.String)
    password = db.Column(db.String)


user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'password': fields.String,
}


class Sensor(db.Model):
    __tablename__ = 'sensors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


sensor_fields = {
    'id': fields.Integer,
    'name': fields.String
}


@app.route('/', methods=['POST'])
def post_measurement():
    data = request.get_json()
    data = json.loads(data)

    if 'date' in data:
        date = data['date']
    else:
        date = datetime.datetime.now().strftime("%d/%m/%Y")
    if 'time' in data:
        time = data['time']
    else:
        time = datetime.datetime.now().strftime("%H:%M:%S")

    new_measurement = Measurement(
        degrees=data['degrees'], humidity=data['humidity'], date=date, time=time, sensor_id=data['sensor_id'])

    db.session.add(new_measurement)
    db.session.commit()

    return jsonify({'message': 'New measurement created!'})

# crud for users


@marshal_with(user_fields)
@app.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all()

    return users


@marshal_with(user_fields)
@app.route('/user/<id>', methods=['GET'])
def get_one_user(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({'message': 'No user found!'})

    return user


@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(public_id=str(uuid.uuid4()),
                    username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created!'})


@app.route('/user/<id>', methods=['PUT'])
def edit_user(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({'message': 'No user found!'})

    data = request.get_json()
    user.username = data['username']
    user.password = generate_password_hash(data['password'], method='sha256')
    db.session.commit()

    return jsonify({'message': 'The user has been updated!'})


@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({'message': 'No user found!'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'The user has been deleted!'})


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        return jsonify({'message': 'Wrong password!'})

    if check_password_hash(user.password, data['password']):
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token': token.decode('UTF-8')})

    else:
        return jsonify({'message': 'Wrong password!'})


# crud for sensors
@marshal_with(sensor_fields)
@app.route('/sensor', methods=['GET'])
def get_all_sensors():
    sensors = Sensor.query.all()

    return sensors


@marshal_with(sensor_fields)
@app.route('/sensor/<id>', methods=['GET'])
def get_one_sensor(id):
    sensor = Sensor.query.filter_by(id=id).first()
    if not sensor:
        return jsonify({'message': 'No sensor found!'})

    return sensor


@app.route('/sensor', methods=['POST'])
def create_sensor():
    data = request.get_json()
    new_sensor = Sensor(name=data['name'])
    db.session.add(new_sensor)
    db.session.commit()
    return jsonify({'message': 'New sensor created!'})


@app.route('/sensor/<id>', methods=['PUT'])
def edit_sensor(id):
    sensor = Sensor.query.filter_by(id=id).first()
    if not sensor:
        return jsonify({'message': 'No sensor found!'})
    data = request.get_json()
    sensor.name = data['name']
    db.session.commit()
    return jsonify({'message': 'The sensor has been updated!'})


@app.route('/sensor/<id>', methods=['DELETE'])
def delete_sensor(id):
    sensor = Sensor.query.filter_by(id=id).first()
    if not sensor:
        return jsonify({'message': 'No sensor found!'})
    db.session.delete(sensor)
    db.session.commit()
    return jsonify({'message': 'The sensor has been deleted!'})

# crud for measurements


@marshal_with(measurement_fields)
@app.route('/measurement', methods=['GET'])
def get_all_measurements():
    measurements = Measurement.query.all()

    return measurements


@marshal_with(measurement_fields)
@app.route('/measurement/<id>', methods=['GET'])
def get_one_measurement(id):
    measurement = Measurement.query.filter_by(id=id).first()
    if not measurement:
        return jsonify({'message': 'No measurement found!'}), 404

    return measurement


@app.route('/measurement', methods=['POST'])
def create_measurement():
    data = request.get_json()
    time = datetime.datetime.now().strftime("%H:%M:%S")
    date = datetime.datetime.now().strftime("%d/%m/%Y")
    new_measurement = Measurement(
        degrees=data['degrees'], humidity=data['humidity'], date=date, time=time, sensor_id=data['sensor_id'])
    db.session.add(new_measurement)
    db.session.commit()
    return jsonify({'message': 'New measurement created!'})


@app.route('/measurement/<id>', methods=['PUT'])
def edit_measurement(id):
    measurement = Measurement.query.filter_by(id=id).first()
    if not measurement:
        return jsonify({'message': 'No measurement found!'})
    data = request.get_json()
    measurement.degrees = data['degrees']
    measurement.humidity = data['humidity']
    measurement.sensor_id = data['sensor_id']
    db.session.commit()
    return jsonify({'message': 'The measurement has been updated!'})


@app.route('/measurement/<id>', methods=['DELETE'])
def delete_measurement(id):
    measurement = Measurement.query.filter_by(id=id).first()
    if not measurement:
        return jsonify({'message': 'No measurement found!'})
    db.session.delete(measurement)
    db.session.commit()
    return jsonify({'message': 'The measurement has been deleted!'})


@marshal_with(measurement_fields)
@app.route('/measurement/daily', methods=['GET'])
def get_daily_measurements():
    """ Returns all measurements from the last 24 hours
        Aggregates measurements by 15 minutes
    """
    data = request.get_json()

    today = datetime.datetime.now().strftime("%d-%m-%Y")

    measurements = Measurement.query.filter_by(
        sensor_id=data['sensor_id'], date=today).all()

    aggregated_measurements = aggregate_measurements(measurements, 15)

    return aggregated_measurements


@marshal_with(measurement_fields)
@app.route('/measurement/weekly', methods=['GET'])
def get_weekly_measurements():
    """ Returns all measurements from the last 7 days
        Aggregates measurements by 6 hours
    """
    data = request.get_json()

    measurements = Measurement.query.filter_by(
        sensor_id=data['sensor_id']).all()

    weekly_measurement = []

    for measurement in measurements:
        if datetime.datetime.strptime(measurement.date, "%d-%m-%Y") >= datetime.datetime.now() - datetime.timedelta(days=7):
            weekly_measurement.append(measurement)

    aggregated_measurements = aggregate_measurements(weekly_measurement, 180)

    return aggregated_measurements


@marshal_with(measurement_fields)
@app.route('/measurement/monthly', methods=['GET'])
def get_monthly_measurements():
    """ Returns all measurements from the last 30 days
        Aggregates measurements by 1 day
    """
    data = request.get_json()

    measurements = Measurement.query.filter_by(sensor_id=data['sensor_id']).filter(
        Measurement.date >= datetime.datetime.now() - datetime.timedelta(days=30)).all()

    aggregated_measurements = aggregate_measurements(measurements, 360)

    return aggregated_measurements


def aggregate_measurements(measurements, interval):
    """ Aggregates measurements by interval in minutes
    """
    aggregated_measurements = []

    current_datetime_slot = datetime.datetime.strptime(
        measurements[0].date + " " + measurements[0].time, "%d-%m-%Y %H:%M:%S")

    tracking_measurements = []

    for measurement in measurements:
        date_time = datetime.datetime.strptime(
            measurement.date + " " + measurement.time, "%d-%m-%Y %H:%M:%S")
        # if within the current time slot, add to tracking_measurements

        if date_time <= current_datetime_slot + datetime.timedelta(minutes=interval):
            tracking_measurements.append(
                {
                    "id": measurement.id,
                    "degrees": measurement.degrees,
                    "humidity": measurement.humidity,
                    "date": measurement.date,
                    "time": measurement.time,
                    "sensor_id": measurement.sensor_id
                }
            )
        # if not within the current time slot, aggregate the tracking_measurements and reset
        elif len(tracking_measurements) > 0:

            avg_degrees = 0
            avg_humidity = 0

            for tracking_measurement in tracking_measurements:
                avg_degrees += tracking_measurement['degrees']
                avg_humidity += tracking_measurement['humidity']

            avg_degrees = avg_degrees / len(tracking_measurements)
            avg_humidity = avg_humidity / len(tracking_measurements)

            aggregated_measurements.append(
                {
                    "id": tracking_measurements[0]['id'],
                    "degrees": round(avg_degrees, 2),
                    "humidity": round(avg_humidity, 2),
                    "date": tracking_measurements[0]['date'],
                    "time": tracking_measurements[0]['time'],
                    "sensor_id": tracking_measurements[0]['sensor_id']
                }
            )

            current_datetime_slot += datetime.timedelta(minutes=interval)
            tracking_measurements = []

    return aggregated_measurements


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True, port=5050)
