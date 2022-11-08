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

temperature_fields = {
    'id': fields.Integer,
    'degrees': fields.Float,
    'date': fields.String,
    'time': fields.String
}

date_fields = {
    'date': fields.String,
    'time': fields.String
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
    'last_login': fields.String
}

class SensorModel(db.Model):
    __tablename__ = 'sensors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    location = db.Column(db.String)
    last_temp = db.Column(db.Float(precision=2))
    last_send = db.Column(db.String)

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
    def __init__(self):
        self.conn = sqlite3.connect('data.db')
        self.cur = self.conn.cursor()
        self.sensor_fails = 0
  
    @marshal_with(temperature_fields)
    def get(self):
        headers = request.headers
        page = int(headers['page'])
        per_page = int(headers['per_page'])
        date = headers['selected_date']
        if date == '':
            data = TemperatureModel.query.paginate(page=page, per_page=per_page)
            return data.items, 200

        else:
            date = headers['selected_date']
            data = TemperatureModel.query.filter_by(date=date).all()
            return data, 200


        
    def post(self):
        input_json = request.get_json(force=True)
 
        temp = round(float(input_json['degrees']), 2)

        #if json does not have date
        if 'date' not in input_json or input_json['date'] == "":
            date = datetime.date.today()
        else:
            date = input_json['date']

        if 'time' not in input_json or input_json['time'] == "":
            time = datetime.datetime.now().strftime("%H:%M:%S")
        else:
            time = input_json['time']


        data = TemperatureModel(degrees=temp, date=date, time=time)
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
        data = TemperatureModel.query.filter_by(id=id).first()
        if data:
            data.degrees = degrees
            db.session.commit()
            return "succes", 200
        return "unauthorized", 401


class Pagination(Resource):
    def get(self):
        headers = request.headers
        page = int(headers['page'])
        per_page = int(headers['per_page'])
        date = headers['selected_date']
        if date == '':
            data = TemperatureModel.query.paginate(page=page, per_page=per_page)
        else:
            data = TemperatureModel.query.filter_by(date=date).paginate(page=page, per_page=per_page)

        p = data.total/per_page
        return math.ceil(p), 200
     
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

class Daily(Resource):
    @marshal_with(temperature_fields)
    def get(self):
        result = TemperatureModel.query.filter(TemperatureModel.date==datetime.date.today()).all()
        return result

class Weekly(Resource):
    def __init__(self):
        self.conn = sqlite3.connect('data.db')
        self.cur = self.conn.cursor()

    @marshal_with(temperature_fields)
    def get(self):
        max_id = TemperatureModel.query.order_by(TemperatureModel.id.desc()).first().id
        min_id = max_id - 11000
        data = TemperatureModel.query.filter(TemperatureModel.id > min_id).all()

        counter = 0
        total_temp = 0
        temps = []
        temp_dict = {}
        last_week = datetime.datetime.now() - datetime.timedelta(days=7)
        max_counter = 10800

        for i in data:
            datetime_string = i.date
            datetimeobj=datetime.datetime.strptime(datetime_string, "%Y-%m-%d")
            if datetimeobj >= last_week:

                counter += 1
                total_temp += i.degrees

                if counter == max_counter:
                    temp_dict = i
                    temp_dict.degrees = round(total_temp / counter, 2)
                    print(temp_dict)
                    temps.append(temp_dict)
                    counter = 0
                    total_temp = 0

        return temps, 200
    
    def post(self):
        input_json = request.get_json(force=True)
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()

        temp = round(input_json['degrees'], 2)

        date = datetime.date.today()
        time = datetime.datetime.now().strftime("%H:%M:%S")

        avgtemp = get_last_temp()

        max_deviation = 1.5

        if temp > avgtemp + max_deviation or temp < avgtemp - max_deviation:
            
            temp = avgtemp
            
        cur.execute(f"INSERT INTO temperatures (degrees, date, time) VALUES ({temp}, '{date}', '{time}')")
        conn.commit()
        conn.close()

        return "succes", 200

class Monthly(Resource):
    @marshal_with(temperature_fields)
    def get(self):
        max_id = TemperatureModel.query.order_by(TemperatureModel.id.desc()).first().id
        min_id = max_id - 40300
        data = TemperatureModel.query.filter(TemperatureModel.id > min_id).all()

        counter = 0
        total_temp = 0
        temps = []
        temp_dict = {}
        last_month = datetime.datetime.now() - datetime.timedelta(days=30)
        max_counter = 21600

        for i in data:
            datetime_string = i.date
            datetimeobj=datetime.datetime.strptime(datetime_string, "%Y-%m-%d")
            if datetimeobj >= last_month:
                counter += 1
                total_temp += i.degrees

                if counter == max_counter:
                    temp_dict = i
                    temp_dict.degrees = round(total_temp / counter, 2)
                    temps.append(temp_dict)
                    counter = 0
                    total_temp = 0

        return temps, 200

class CurrentTemp(Resource):

    def __init__(self):
        self.conn = sqlite3.connect('data.db')
        self.cur = self.conn.cursor()
        f = open("pw.txt","r")
        t = open("token.txt","r")
        self.password = f.readlines()[0]
        self.token = t.readlines()[0]
        f.close()
        t.close()

    def get(self):
            self.cur.execute("select * from temperatures order by id desc limit 5")

            result = json.dumps(self.cur.fetchall())
            result_json = json.loads(result)

            return result_json, 200


def get_last_temp():
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    cur.execute("SELECT degrees FROM temperatures ORDER BY id DESC LIMIT 3")
    
    temps = cur.fetchall()
    avg_temp = 0
    for i in temps:
        avg_temp += i[0]

    avg_temp = round(avg_temp / len(temps), 2)
    conn.close()
    return avg_temp

class Visitor(Resource):

    def post(self):
        t = open("visitors.txt","r")
        visitors = t.readlines()[0]
        t.close()

        f = open("visitors.txt","w")
        f.write(str(int(visitors) + 1))
        f.close()

        return int(visitors) + 1

class Extra(Resource):

    @marshal_with(extra_fields)
    def get(self):
        result = ExtraModel.query.order_by(ExtraModel.id.desc()).first()
        
        return result, 200

    def post(self):
        input_json = request.get_json(force=True)
        data = ExtraModel(
            current_temp = input_json['current_temp'],
            monthly_average = input_json['monthly_average'],
            weekly_average=input_json['weekly_average'],
            daily_average=input_json['daily_average'],
            average_yesterday=input_json['average_yesterday'],
            date=datetime.date.today(),
            time=datetime.datetime.now().strftime("%H:%M:%S")
        )
        db.session.add(data)
        db.session.commit()
        return 200

class Dates(Resource):
    @marshal_with(date_fields)
    def get(self):
        dates = TemperatureModel.query.with_entities(TemperatureModel.date).distinct().all()
        return dates, 200

api.add_resource(Temperature, "/")
api.add_resource(Dates, "/dates")
api.add_resource(Daily, "/daily")
api.add_resource(Weekly, "/weekly")
api.add_resource(Monthly, "/monthly")
api.add_resource(CurrentTemp, "/current_temp")
api.add_resource(Login, "/login")
api.add_resource(Visitor, "/visitors")
api.add_resource(User, "/user")
api.add_resource(Extra, "/extra")
api.add_resource(Pagination, "/last_page")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='192.168.178.69',port=1000, debug=True, threaded=True)