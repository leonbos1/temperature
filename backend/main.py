import json
from flask import Flask, request
import sqlite3
import json

app = Flask(__name__)
@app.route('/', methods=['GET'])
def index():

    if request.headers['kaas'] == 'yoyokaas':
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        cur.execute("select * from temperatures")
        result = json.dumps(cur.fetchall())

        con.close()

        return result

@app.route('/', methods=["POST"])
def post():
    input_json = request.get_json(force=True) 

    con = sqlite3.connect('data.db')
    cur = con.cursor()

    temp = input_json['degrees']
    date = input_json['date']
    time = input_json['time']

    cur.execute(f"insert into temperatures ('degrees', 'date', 'time') values ('{temp}','{date}','{time}')")

    con.commit()

    con.close()

    return 'success'

app.run(debug=True)