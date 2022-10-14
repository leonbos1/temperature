import json
from flask import Flask, request
import sqlite3
import json
import datetime
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def index():
    return "", 404

@app.route('/<id>', methods=['DELETE'])
def delete(id):
    if request.headers['token'] == 'ABHJ':
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute(f"DELETE FROM temperatures WHERE id = {id}")
        conn.commit()
        conn.close()
        return "succes", 200

    return "unauthorized", 401

@app.route('/',methods=['POST'])
def post():
    try:
        input_json = request.get_json(force=True)
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()

        temp = round(input_json['degrees'], 2)

        date = datetime.date.today()
        time = datetime.datetime.now().strftime("%H:%M:%S")

        avgtemp = get_last_temp()

        max_deviation = 1.5

        if avgtemp + max_deviation < temp or avgtemp - max_deviation > temp:
            cur.execute(f"INSERT INTO temperatures (degrees, date, time) VALUES ({temp}, '{date}', '{time}')")
            conn.commit()
            conn.close()
            return "succes", 200

        return "unauthorized", 401

    except:
        return "unauthorized", 401

def get_last_temp():
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    cur.execute("SELECT temperature FROM temperatures ORDER BY id DESC LIMIT 3")
    
    temps = cur.fetchall()
    avg_temp = 0
    for i in temps:
        avg_temp += i[0]

    avg_temp = round(avg_temp / len(temps), 2)
    conn.close()
    return avg_temp

@app.route('/<id>', methods=['PUT'])
def put(id):
    if request.headers['token'] == 'ABHJ':
        input_json = request.get_json(force=True)
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute(f"UPDATE temperatures SET degrees = {input_json['degrees']} WHERE id = {id}")
        conn.commit()
        conn.close()
        return "succes", 200

    return "unauthorized", 401

@app.route('/current_temp', methods=['GET'])
def current_temp():

    if request.headers['token'] == 'ABHJ':
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        cur.execute("select * from temperatures order by id desc limit 5")

        result = json.dumps(cur.fetchall())
        result_json = json.loads(result)

        avg_temp = 0

        for e in result_json:
            avg_temp += e[1]

        con.close()

        return str(round(avg_temp/5,2))

    return "unauthorized", 401

@app.route('/weekly', methods=["GET"])
def weekly():
    if request.headers['token'] == 'ABHJ':
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        cur.execute("select * from temperatures order by id asc limit 10500")

        result = json.dumps(cur.fetchall())

        con.close()

        result_json = json.loads(result)

        today = datetime.datetime.now()

        last_week = today - datetime.timedelta(days=7)

        to_return = []

        for e in result_json:
            datetime_string = e[2]
            datetimeobj=datetime.datetime.strptime(datetime_string, "%Y-%m-%d")
            
            if datetimeobj >= last_week:
                to_return.append(e)
        
        return json.dumps(str(to_return))
    
    return "unauthorized", 401


app.run(host='192.168.178.220', debug=False)
