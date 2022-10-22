import json
from flask import Flask, request
import sqlite3
import json
import datetime
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from sqlalchemy import *
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
api = Api(app)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SECRET_KEY'] = 'secretkey'
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
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
    last_login = db.Column(db.String(20))


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

    def delete(self):
        try:
            if request.headers['token'] == self.token:
                input_json = request.get_json(force=True)
                self.cur.execute(f"DELETE FROM temperatures WHERE id = {input_json['id']}")
                self.conn.commit()
                return "succes", 200
        except:
            return "unauthorized", 401



    def put(self):
        try:
            if request.headers['token'] == self.token:
                input_json = request.get_json(force=True)
                data = TemperatureModel.query.filter_by(id=input_json['id']).first()
                if data is not None:
                    data.degrees = input_json['degrees']
                    db.session.commit()
                    return "succes", 200
                return "unauthorized", 401

            return "unauthorized", 401
        except:
            return "unauthorized", 401
        


class Login(Resource):
    def post(self):
        
        input_json = request.get_json(force=True)
        username = input_json['username']
        password = input_json['password']
        user = UserModel.query.filter_by(username=username).first()
        if user is not None:
            if user.password == password:
                user.last_login = datetime.datetime.now().strftime("%H:%M:%S")
                db.session.commit()

                #TODO token generation 
                return "Some token", 200

            return "unauthorized", 401
        return "unauthorized", 401


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


if __name__ == "__main__":
    app.run(host='192.168.178.69',port=1000, debug=True, threaded=True)