import sqlite3
from time import sleep

def main():
    while True:
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute("SELECT degrees, date, time FROM temperatures LIMIT 40500")

        data = cur.fetchall()

        current_date = data[0][1]
        temps = []

        temperature_per_day = {}

        for i in data:
            if current_date == i[1]:
                temps.append(i[0])
            else:
                temperature_per_day[current_date] = round(sum(temps) / len(temps),2)
                current_date = i[1]
                temps = []
            
            if i == data[-1]:
                temperature_per_day[current_date] = round(sum(temps) / len(temps),2)


        cur.execute("DELETE FROM average_temperatures")
        conn.commit()

        for i in temperature_per_day:
            print(i, temperature_per_day[i])
            cur.execute("INSERT INTO average_temperatures VALUES (?,?)", (i, temperature_per_day[i]))

        conn.commit()
        conn.close()
        sleep(60)

if __name__ == "__main__":
    main()