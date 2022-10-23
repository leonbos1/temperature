from cgitb import reset
import json
from math import degrees
from flask import Flask, request, jsonify, make_response
import sqlite3
import datetime
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api, marshal_with, fields
from sqlalchemy import *
from flask_sqlalchemy import SQLAlchemy
import os
from functools import wraps
import jwt
import bcrypt
import string
import random

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
    date = db.Column(db.String(20))
    time = db.Column(db.String(20))

class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String, unique=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
    last_login = db.Column(db.String(20))

user_data = {
    'id': fields.Integer,
    'username': fields.String,
    'last_login': fields.String
}

class SensorModel(db.Model):
    __tablename__ = 'sensors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    location = db.Column(db.String(20))
    last_temp = db.Column(db.Float(precision=2))
    last_send = db.Column(db.String(20))

class CurrentTempModel(db.Model):
    __tablename__ = 'current_temp'
    id = db.Column(db.Integer, primary_key=True)
    degrees = db.Column(db.Float(precision=2))
    date = db.Column(db.String(20))
    time = db.Column(db.String(20))

class DailyAverageModel(db.Model):
    __tablename__ = 'daily_average'
    id = db.Column(db.Integer, primary_key=True)
    degrees = db.Column(db.Float(precision=2))
    date = db.Column(db.String(20))
    time = db.Column(db.String(20))

class WeeklyAverageModel(db.Model):
    __tablename__ = 'weekly_average'
    id = db.Column(db.Integer, primary_key=True)
    degrees = db.Column(db.Float(precision=2))
    date = db.Column(db.String(20))
    time = db.Column(db.String(20))

class MonthlyAverageModel(db.Model):
    __tablename__ = 'monthly_average'
    id = db.Column(db.Integer, primary_key=True)
    degrees = db.Column(db.Float(precision=2))
    date = db.Column(db.String(20))
    time = db.Column(db.String(20))

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
        f = open("pw.txt","r")
        t = open("token.txt","r")
        self.password = f.readlines()[0]
        self.token = t.readlines()[0]
        f.close()
        t.close()
        self.sensor_fails = 0
        
    #@token_required add this when esp32 code is updated
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
        
    def get(self):
        return "", 404

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
        try:
            input_json = request.get_json(force=True)
            id = input_json['id']
            degrees = input_json['degrees']
            data = TemperatureModel.query.filter_by(id=id).first()
            if data:
                data.degrees = degrees
                db.session.commit()
                return "succes", 200
            return "unauthorized", 401

        except:
            return "unauthorized", 401
        
class User(Resource):
    def id_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    @marshal_with(user_data)
    @token_required
    def get(self, current_user):
   
        return UserModel.query.all()

    #@token_required add this when first user is made in production
    def post(self):
        """register user
        """
        args = request.get_json(force=True)
        data = UserModel(
            public_id=self.id_generator(80),
            username=args['username'],
            password=bcrypt.hashpw(args['password'].encode('utf-8'), salt=bcrypt.gensalt()),
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
            user = UserModel.query.filter(UserModel.username==username).first()

            if user:
                if bcrypt.checkpw(password.encode('utf-8'), user.password):
                    token = jwt.encode({'public_id': user.public_id}, app.config['SECRET_KEY'], algorithm='HS256')
                    return jsonify({'token': token, 'user': user.username})

                if user.password == password:
                    user.last_login = datetime.datetime.now().strftime("%H:%M:%S")
                    db.session.commit()

                    #TODO token generation 
                    return "Some token", 200

                return "unauthorized", 401
            
            return "unauthorized", 401

        #except:
         #   return "unauthorized", 401

class Weekly(Resource):
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
        max_id = self.cur.execute("select * from temperatures order by id asc limit 10500").fetchall()[-1][0]
        min_id = max_id - 10050
        data = self.cur.execute(f"select * from temperatures where id > {min_id}").fetchall()
        result = json.dumps(data)

        result_json = json.loads(result)
        today = datetime.datetime.now()
        last_week = today - datetime.timedelta(days=7)

        to_return = []

        for e in result_json:
            datetime_string = e[2]
            datetimeobj=datetime.datetime.strptime(datetime_string, "%Y-%m-%d")
            
            if datetimeobj >= last_week:
                to_return.append(e)
        
        return to_return, 200

    
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

            avg_temp = 0

            for e in result_json:
                avg_temp += e[1]

            return round(avg_temp/5,2)


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

api.add_resource(Temperature, "/")
api.add_resource(Weekly, "/weekly")
api.add_resource(CurrentTemp, "/current_temp")
api.add_resource(Login, "/login")
api.add_resource(Visitor, "/visitors")
api.add_resource(User, "/user")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='192.168.178.69',port=1000, debug=True, threaded=True)