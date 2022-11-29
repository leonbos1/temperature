import sqlite3
from time import sleep

def main():
    while True:
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute("DELETE FROM average_temperatures")
        conn.commit()
        try:
            sensors = cur.execute('SELECT id FROM sensors').fetchall()

            for i in sensors:
                data = cur.execute('SELECT degrees, date, time FROM temperatures WHERE sensor_id = ? ORDER BY date desc', (i[0],)).fetchall()
                #print(data)
                data = data[::-1]

                current_date = data[0][1]
                temps = []

                temperature_per_day = {}

                for j in data:
                    if current_date == j[1]:
                        temps.append(j[0])
                    else:
                        temperature_per_day[current_date] = round(sum(temps) / len(temps),2)
                        current_date = j[1]
                        temps = []
                    if j == data[-1]:
                        temperature_per_day[current_date] = round(sum(temps) / len(temps),2)

                for day in temperature_per_day:
                    cur.execute('INSERT INTO average_temperatures (sensor_id, date, degrees) VALUES (?,?,?)', (i[0], day, temperature_per_day[day]))

                conn.commit()
            sleep(60)
        except:
            sleep(60)

if __name__ == "__main__":
    main()