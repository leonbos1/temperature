import random
import datetime
import requests
import json

url = "http://192.168.178.69:1000"
delta = 50

today = datetime.datetime.now() - datetime.timedelta(days=delta)

def main():
    for i in range(0,delta):
        for j in range(60):

            data = {
                "degrees" : random.randint(15, 20),
                "date" : (today + datetime.timedelta(days=i)).strftime("%Y-%m-%d"),
                "time" : (datetime.datetime.now() - datetime.timedelta(minutes=j*10)).strftime("%H:%M:%S")
            }
            
            response = requests.post(url, data=json.dumps(data))

if __name__ == "__main__":
    main()
