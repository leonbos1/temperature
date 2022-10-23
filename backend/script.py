import requests
import time

url2 = "http://ronleon.nl:5000"
url = "http://192.168.178.69:1000"


def main():
    monthly_average = get_monthly_average()
    weekly_average = get_weekly_average()
    daily_average = get_daily_average()
    current_temp = get_current_temp()

    data = {
        "weekly_average":weekly_average,
    "daily_average":daily_average,
    "monthly_average":monthly_average,
    "current_temp":current_temp
    }

    add_to_db(data)

def get_current_temp():
    response = requests.get(url + "/current_temp")
    all_temps = []
    for temp in response.json():
        all_temps.append(temp[1])

    return round(all_temps[0],2)

def get_weekly_average():
    response = requests.get(url + "/weekly")
    all_temps = []
    for temp in response.json():
        all_temps.append(temp[1])
    average = sum(all_temps) / len(all_temps)

    return round(average,2)

def get_daily_average():
    response = requests.get(url + "/weekly")
    all_temps = []
    reversed_response = response.json()[::-1]
    today = reversed_response[0][2]

    for temp in reversed_response:
        if temp[2] != today:
            return round(sum(all_temps) / len(all_temps),2)
        all_temps.append(temp[1])
    average = sum(all_temps) / len(all_temps)

    return round(average,2)

def get_monthly_average():
    response = requests.get(url + "/weekly")
    all_temps = []
    for temp in response.json():
        all_temps.append(temp[1])
    average = sum(all_temps) / len(all_temps)

    return round(average,2)

def add_to_db(data):
    response = requests.post(url+"/extra",json=data)


if __name__ == "__main__":
    while True:
        main()
        time.sleep(60)