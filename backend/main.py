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
import math

app = Flask(__name__)
api = Api(app)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SECRET_KEY'] = 'secretkey'
regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
db = SQLAlchemy(app)

class TemperatureModel(db.Model):
    __tablename__ = 'temperatures'
    id = db.Column(db.Integer, primary_key=True)
    degrees = db.Column(db.Float(precision=2))
    date = db.Column(db.String)
    time = db.Column(db.String)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id'))

temperature_fields = {
    'id': fields.Integer,
    'degrees': fields.Float,
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

class AverageTemperatures(db.Model):
    __tablename__ = 'average_temperatures'
    date = db.Column(db.String, primary_key=True)
    degrees = db.Column(db.Float(precision=2))
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id'))

average_fields = {
    'date': fields.String,
    'degrees': fields.Float,
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
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = UserModel.query.filter_by(public_id=data['public_id']).first()
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
        date = request.args.get('selected_date', 1, type=str)
        sensor_id = request.args.get('sensor_id', 1, type=int)

        #TODO filter by sensor id
        if date == '':
            data = TemperatureModel.query.paginate(page=page, per_page=per_page)
            return data.items, 200

        else:
            data = TemperatureModel.query.filter_by(date=date).all()
            return data, 200


        
    def post(self):
        input_json = request.get_json(force=True)
 
        temp = round(float(input_json['degrees']), 2)
        sensor_id = input_json['sensor_id']

        #if json does not have date
        if 'date' not in input_json or input_json['date'] == "":
            date = datetime.date.today()
        else:
            date = input_json['date']

        if 'time' not in input_json or input_json['time'] == "":
            time = datetime.datetime.now().strftime("%H:%M:%S")
        else:
            time = input_json['time']


        data = TemperatureModel(degrees=temp, date=date, time=time, sensor_id=sensor_id)
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
        sensor_id = input_json['sensor_id']
        data = TemperatureModel.query.filter_by(id=id).first()
        if data:
            data.degrees = degrees
            data.sensor_id = sensor_id
            db.session.commit()
            return "succes", 200
        return "unauthorized", 401

@app.route('/last_page')
def pagination():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 1, type=int)
    date = request.args.get('selected_date', 1, type=str)
    sensor_id = request.args.get('sensor_id', 1, type=int)

    if date == '':
        data = TemperatureModel.query.paginate(page=page, per_page=per_page).filter_by(sensor_id=sensor_id)
    else:
        data = TemperatureModel.query.filter_by(date=date).paginate(page=page, per_page=per_page).filter_by(sensor_id=sensor_id)

    p = data.total/per_page
    #return a json
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

    #@token_required add this when first user is made in production
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
        password=input_json['password']

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
            user = UserModel.query.filter(UserModel.username==username).first()

            if user:
                if password == user.password:
                    token = jwt.encode({'public_id': user.public_id}, app.config['SECRET_KEY'], algorithm='HS256')
                    return jsonify({'token': token, 'user': user.username})
                return "unauthorized", 401
            
            return "unauthorized", 401

        #except:
         #   return "unauthorized", 401

@app.route('/temperature/daily')
@marshal_with(temperature_fields)
def daily():
    #TODO run this in production to update legacy entries
    # TemperatureModel.query.filter_by(sensor_id=None).update({TemperatureModel.sensor_id: 1})
    # AverageTemperatures.query.filter_by(sensor_id=None).update({AverageTemperatures.sensor_id: 1})
    # db.session.commit()
    sensor_id = request.args.get('sensor_id', 1, type=int)
    result = TemperatureModel.query.filter_by(sensor_id=sensor_id).filter(TemperatureModel.date==datetime.date.today()).all()
    data = []
    temp = 0
    counter = 0

    for i in result:
        temp += i.degrees
        counter += 1
        if counter > 15:
            i.degrees = temp/counter
            data.append(i)
            temp = 0
            counter = 0

    return data, 200

@app.route('/checklogin')
def check_login():
    headers = request.headers
    token = headers['token']
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return "succes", 200
    except:
        return "unauthorized", 401

@app.route('/temperature/weekly')
@marshal_with(average_fields)
def weekly():
    #last 7 days
    sensor_id = request.args.get('sensor_id', 1, type=int)
    data = AverageTemperatures.query.filter(AverageTemperatures.date >= datetime.date.today() - datetime.timedelta(days=7)).filter_by(sensor_id=sensor_id).all()
    return data, 200

@app.route('/temperature/monthly')
@marshal_with(average_fields)
def monthly():
    sensor_id = request.args.get('sensor_id', 1, type=int)
    data = AverageTemperatures.query.filter_by(sensor_id=sensor_id).all()
    return data, 200

@app.route('/temperature/current')
def current_temperature():
    #TODO figure out a way to make this work with multiple sensors
    result = TemperatureModel.query.order_by(TemperatureModel.id.desc()).limit(3).all()
    temp = 0
    for i in result:
        temp += i.degrees
    current_temp = round(temp/3, 2)

    result = TemperatureModel.query.filter(TemperatureModel.date==datetime.date.today()).all()
    temps_today = []
    for i in result:
        temps_today.append(i.degrees)
    daily_average = round(sum(temps_today)/len(temps_today), 2)

    result = TemperatureModel.query.filter(TemperatureModel.date==datetime.date.today() - datetime.timedelta(days=1)).all()
    temps_yesterday = []
    for i in result:
        temps_yesterday.append(i.degrees)
    average_yesterday = round(sum(temps_yesterday)/len(temps_yesterday), 2)

    data = {
        'current_temp': current_temp,
        'daily_average': daily_average,
        'average_yesterday': average_yesterday
    }
    
    return data, 200

@app.route('/visitors', methods=['POST'])
def update_visitors():
    #TODO fix this
    t = open("visitors.txt","r")
    visitors = t.readlines()[0]
    t.close()

    f = open("visitors.txt","w")
    f.write(str(int(visitors) + 1))
    f.close()
    #make it return a json atleast
    return int(visitors) + 1, 200

@app.route('/dates')
@marshal_with(date_fields)
def dates():
    dates = TemperatureModel.query.with_entities(TemperatureModel.date).distinct().all()
    return dates, 200

api.add_resource(Temperature, "/")
api.add_resource(Login, "/login")
api.add_resource(User, "/user")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='192.168.178.69',port=1000, debug=True, threaded=True)