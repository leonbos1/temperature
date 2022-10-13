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

    if request.headers['kaas'] == 'yoyokaas':
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        cur.execute("select * from temperatures")
        result = json.dumps(cur.fetchall())

        con.close()

        return result

@app.route('/current_temp', methods=['GET'])
def current_temp():

    if request.headers['kaas'] == 'yoyokaas':
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


@app.route('/', methods=["POST"])
def post():
    input_json = request.get_json(force=True)

    con = sqlite3.connect('data.db')
    cur = con.cursor()

    temp = round(input_json['degrees'], 2)

    date = datetime.date.today()
    time = datetime.datetime.now()
    current_time = time.strftime("%H:%M:%S")

    cur.execute(
        f"insert into temperatures ('degrees', 'date', 'time') values ('{temp}','{date}','{current_time}')")

    con.commit()

    con.close()

    return 'success'


@app.route('/weekly', methods=["GET"])
def weekly():
    if request.headers['kaas'] == 'yoyokaas':
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        cur.execute("select * from temperatures")
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


app.run(host='192.168.178.69', debug=True)
