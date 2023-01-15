import sqlite3
from time import sleep

def main():
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute("DELETE FROM average_temperatures")
        conn.commit()

        #write to test.txt
        f = open("test.txt", "w")
        f.write("test123")
        f.close()

        try:
            sensors = cur.execute('SELECT id FROM sensors').fetchall()

            for i in sensors:
                data = cur.execute('SELECT degrees, humidity, date, time FROM temperatures WHERE sensor_id = ? ORDER BY date desc', (i[0],)).fetchall()
                #print(data)
                data = data[::-1]

                current_date = data[0][2]
                temps = []
                humidity = []

                temperature_per_day = {}
                humidity_per_day = {}

                for j in data:
                    if current_date == j[2]:
                        temps.append(j[0])
                        humidity.append(j[1])
                    else:
                        temperature_per_day[current_date] = round(sum(temps) / len(temps),2)
                        humidity_per_day[current_date] = round(sum(humidity) / len(humidity),2)
                        current_date = j[2]
                        temps = []
                        humidity = []
                    if j == data[-1]:
                        temperature_per_day[current_date] = round(sum(temps) / len(temps),2)
                        humidity_per_day[current_date] = round(sum(humidity) / len(humidity),2)

                for day in temperature_per_day:
                    cur.execute('INSERT INTO average_temperatures (sensor_id, date, degrees, humidity) VALUES (?,?,?,?)', (i[0], day, temperature_per_day[day], humidity_per_day[day]))

                conn.commit()
        except:
            pass