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


app = Flask(__name__)
api = Api(app)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'data.db')
app.config['SECRET_KEY'] = 'secretkey'
regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
db = SQLAlchemy(app)


class TemperatureModel(db.Model):
    __tablename__ = 'temperatures'
    id = db.Column(db.Integer, primary_key=True)
    degrees = db.Column(db.Float(precision=2))
    humidity = db.Column(db.Float(precision=2))
    date = db.Column(db.String)
    time = db.Column(db.String)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id'))


temperature_fields = {
    'id': fields.Integer,
    'degrees': fields.Float,
    'humidity': fields.Float,
    'date': fields.String,
    'time': fields.String,
    'sensor_id': fields.Integer,
}

date_fields = {
    'date': fields.String,
    'time': fields.String,
}


class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String, unique=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    last_login = db.Column(db.String)


user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'password': fields.String,
    'last_login': fields.String,
}


class SensorModel(db.Model):
    __tablename__ = 'sensors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    location = db.Column(db.String)
    last_temp = db.Column(db.Float(precision=2))
    last_send = db.Column(db.String)


sensor_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'location': fields.String,
    'last_temp': fields.Float,
    'last_send': fields.String,
}


class AverageTemperatures(db.Model):
    __tablename__ = 'average_temperatures'
    date = db.Column(db.String, primary_key=True)
    degrees = db.Column(db.Float(precision=2))
    humidity = db.Column(db.Float(precision=2))
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id'))


average_fields = {
    'date': fields.String,
    'degrees': fields.Float,
    'humidity': fields.Float,
    'sensor_id': fields.Integer,
}


class ExtraModel(db.Model):
    __tablename__ = 'extra'
    id = db.Column(db.Integer, primary_key=True)
    current_temp = db.Column(db.Float(precision=2))
    daily_average = db.Column(db.Float(precision=2))
    weekly_average = db.Column(db.Float(precision=2))
    monthly_average = db.Column(db.Float(precision=2))
    average_yesterday = db.Column(db.Float(precision=2))
    date = db.Column(db.String)
    time = db.Column(db.String)


extra_fields = {
    'id': fields.Integer,
    'current_temp': fields.Float,
    'daily_average': fields.Float,
    'weekly_average': fields.Float,
    'monthly_average': fields.Float,
    'average_yesterday': fields.Float,
    'date': fields.String,
    'time': fields.String
}


def token_required(f):
    """Decorator yo check token
    """
    @wraps(f)
    def decorator(*args, **kwargs):
        global user
        token = None
        current_user = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return 401

        try:
            data = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = UserModel.query.filter_by(
                public_id=data['public_id']).first()
            user = current_user
        except:
            return 401
        return f(current_user, *args, **kwargs)
    return decorator


class Temperature(Resource):

    @marshal_with(temperature_fields)
    def get(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 1, type=int)
        date = request.args.get('selected_date', '', type=str)
        sensor_id = request.args.get('sensor_id', 1, type=int)

        # TODO filter by sensor id
        if date:
            data = TemperatureModel.query.paginate(
                page=page, per_page=per_page)
            return data.items, 200

        if sensor_id:
            data = TemperatureModel.query.filter_by(
                sensor_id=sensor_id).paginate(page=page, per_page=per_page)
            return data.items, 200

        if date and sensor_id:
            data = TemperatureModel.query.filter_by(
                sensor_id=sensor_id).paginate(page=page, per_page=per_page)
            print("here")
            return data.items, 200

        else:
            data = TemperatureModel.query.filter_by(
                date=date).paginate(page=page, per_page=per_page)
            return data.items, 200

    def post(self):
        input_json = request.get_json(force=True)

        temp = round(float(input_json['degrees']), 2)
        humidity = round(float(input_json['humidity']), 2)
        sensor_id = input_json['sensor']

        # if json does not have date, this is for manually adding data in management page
        if 'date' not in input_json or input_json['date'] == "":
            date = datetime.date.today()
        else:
            date = input_json['date']

        if 'time' not in input_json or input_json['time'] == "":
            time = datetime.datetime.now().strftime("%H:%M:%S")
        else:
            time = input_json['time']

        data = TemperatureModel(
            degrees=temp, date=date, time=time, sensor_id=sensor_id, humidity=humidity)
        db.session.add(data)
        db.session.commit()

        return "succes", 200

    @token_required
    def delete(self, current_user):
        try:
            input_json = request.get_json(force=True)
            id = input_json['id']
            data = TemperatureModel.query.filter_by(id=id).first()
            if data:
                db.session.delete(data)
                db.session.commit()
                return "succes", 200
            return 404, "not found"
        except:
            return "unauthorized", 401

    @token_required
    def put(self, current_user):
        input_json = request.get_json(force=True)
        id = input_json['id']
        degrees = input_json['degrees']
        humidity = input_json['humidity']
        sensor_id = input_json['sensor_id']
        data = TemperatureModel.query.filter_by(id=id).first()
        if data:
            data.degrees = degrees
            data.humidity = humidity
            data.sensor_id = sensor_id
            db.session.commit()
            return "succes", 200
        return "unauthorized", 401


@app.route('/last_page', methods=['GET'])
def pagination():
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('per_page', 0, type=int)
    date = request.args.get('selected_date', '', type=str)
    sensor_id = request.args.get('sensor_id', 0, type=int)

    data = TemperatureModel.query.paginate(page=page, per_page=per_page)

    if date:
        data = TemperatureModel.query.filter_by(
            date=date).paginate(page=page, per_page=per_page)
    if sensor_id:
        data = TemperatureModel.query.filter_by(
            sensor_id=sensor_id).paginate(page=page, per_page=per_page)
    if date and sensor_id:
        data = TemperatureModel.query.filter_by(
            date=date, sensor_id=sensor_id).paginate(page=page, per_page=per_page)

    p = data.total/per_page
    result = jsonify({'last_page': math.ceil(p)})
    return result, 200


class User(Resource):
    def id_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    @marshal_with(user_fields)
    @token_required
    def get(self, current_user):
        result = UserModel.query.all()

        return result

    # @token_required add this when first user is made in production
    def post(self):
        """register user
        """
        args = request.get_json(force=True)
        data = UserModel(
            public_id=self.id_generator(80),
            username=args['username'],
            password=args['password'],
        )
        db.session.add(data)
        db.session.commit()
        return 200

    @token_required
    def delete(self, current_user):
        input_json = request.get_json(force=True)
        id = input_json['id']
        result = UserModel.query.filter_by(id=id).first()
        if result:
            db.session.delete(result)
            db.session.commit()
            return "succes", 200
        return "User not found", 404

    @token_required
    def put(self, current_user):
        input_json = request.get_json(force=True)
        id = input_json['id']
        username = input_json['username']
        password = input_json['password']

        result = UserModel.query.filter_by(id=id).first()

        if result:
            result.username = username
            result.password = password
            db.session.commit()
            return "succes", 200

        return "User not found", 404


class Login(Resource):
    def post(self):
       # try:
        input_json = request.get_json(force=True)
        username = input_json['username']
        password = input_json['password']
        user = UserModel.query.filter(UserModel.username == username).first()

        if user:
            if password == user.password:
                token = jwt.encode({'public_id': user.public_id},
                                   app.config['SECRET_KEY'], algorithm='HS256')
                return jsonify({'token': token, 'user': user.username})
            return "unauthorized", 401

        return "unauthorized", 401

        # except:
     #   return "unauthorized", 401


@app.route('/temperature/daily')
@marshal_with(temperature_fields)
def daily():
    sensor_id = request.args.get('sensor_id', 1, type=int)
    result = TemperatureModel.query.filter_by(sensor_id=sensor_id).filter(
        TemperatureModel.date == datetime.date.today()).all()

    data = []
    temp = 0
    humidity = 0
    counter = 0

    for i in result:
        temp += i.degrees
        humidity += i.humidity
        counter += 1
        if counter > 15:
            i.degrees = temp/counter
            i.humidity = humidity/counter
            data.append(i)
            temp = 0
            humidity = 0
            counter = 0

    return data, 200


@app.route('/checklogin')
def check_login():
    headers = request.headers
    token = headers['token']
    try:
        data = jwt.decode(
            token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return "succes", 200
    except:
        return "unauthorized", 401


@app.route('/temperature/weekly')
@marshal_with(average_fields)
def weekly():
    # last 7 days
    sensor_id = request.args.get('sensor_id', 1, type=int)
    data = AverageTemperatures.query.filter(AverageTemperatures.date >= datetime.date.today(
    ) - datetime.timedelta(days=7)).filter_by(sensor_id=sensor_id).all()
    return data, 200


@app.route('/temperature/monthly')
@marshal_with(average_fields)
def monthly():
    sensor_id = request.args.get('sensor_id', 1, type=int)
    data = AverageTemperatures.query.filter_by(sensor_id=sensor_id).all()
    return data, 200


@app.route('/temperature/current')
def current_temperature():
    # current temperature is de average of the last 5 entries
    current_temperature = 0
    current_humidity = 0
    sensor_id = request.args.get('sensor_id', 1, type=int)
    data = TemperatureModel.query.filter_by(sensor_id=sensor_id).order_by(
        TemperatureModel.id.desc()).limit(5).all()
    for i in data:
        current_humidity += i.humidity
        current_temperature += i.degrees

    current_temperature = current_temperature/5
    current_humidity = current_humidity/5

    try:
        all_temperatures_today = TemperatureModel.query.filter_by(
            sensor_id=sensor_id).filter(TemperatureModel.date == datetime.date.today()).all()
        average_temperature_today = 0
        for i in all_temperatures_today:
            average_temperature_today += i.degrees
        average_temperature_today = average_temperature_today / \
            len(all_temperatures_today)

        average_temperature_yesteraday = 0
        all_temperatures_yesterday = TemperatureModel.query.filter_by(sensor_id=sensor_id).filter(
            TemperatureModel.date == datetime.date.today() - datetime.timedelta(days=1)).all()
        for i in all_temperatures_yesterday:
            average_temperature_yesteraday += i.degrees
        average_temperature_yesteraday = average_temperature_yesteraday / \
            len(all_temperatures_yesterday)

    except:
        # TODO fix this
        # currently, if there are no temperatures in the database today/yesterday, the api will crash because of the division by zero
        average_temperature_today = 0
        average_temperature_yesteraday = 0

    data = {
        'current_temp': round(current_temperature, 2),
        'current_humidity': round(current_humidity, 2),
        'daily_average': round(average_temperature_today, 2),
        'average_yesterday': round(average_temperature_yesteraday, 2)
    }

    return data, 200


@app.route('/visitors', methods=['POST'])
def update_visitors():
    t = open("visitors.txt", "r")
    visitors = t.readlines()[0]
    t.close()

    f = open("visitors.txt", "w")
    f.write(str(int(visitors) + 1))
    f.close()
    visit_data = {
        'visitors': int(visitors)+1
    }
    return visit_data, 200


@app.route('/dates')
@marshal_with(date_fields)
def dates():
    dates = TemperatureModel.query.with_entities(
        TemperatureModel.date).distinct().all()
    return dates, 200


@app.route('/sensors')
@marshal_with(sensor_fields)
def get_sensors():
    sensors = SensorModel.query.all()
    return sensors, 200


@app.route('/sensors', methods=['POST'])
@token_required
def add_sensor():
    input_json = request.get_json(force=True)
    name = input_json['name']
    location = input_json['location']
    sensor = SensorModel(
        name=name,
        location=location
    )
    db.session.add(sensor)
    db.session.commit()
    return "succes", 200


@app.route('/sensors', methods=['DELETE'])
@token_required
def delete_sensor():
    input_json = request.get_json(force=True)
    id = input_json['id']
    sensor = SensorModel.query.filter_by(id=id).first()
    if sensor:
        db.session.delete(sensor)
        db.session.commit()
        return "succes", 200
    return "Sensor not found", 404


@app.route('/sensors', methods=['PUT'])
@token_required
def update_sensor():
    input_json = request.get_json(force=True)
    id = input_json['id']
    name = input_json['name']
    location = input_json['location']
    sensor = SensorModel.query.filter_by(id=id).first()
    if sensor:
        sensor.name = name
        sensor.location = location
        db.session.commit()
        return "succes", 200
    return "Sensor not found", 404


api.add_resource(Temperature, "/")
api.add_resource(Login, "/login")
api.add_resource(User, "/user")

if __name__ == "__main__":
    while True:
        try:
            with app.app_context():
                db.create_all()
            app.run(host="192.168.178.220", port=5000,
                    debug=True, threaded=True)
        except Exception as e:
            sleep(10)
