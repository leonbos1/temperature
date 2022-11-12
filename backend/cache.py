import sqlite3

# alle data opslaan tot en met een maand geleden
# van alle dagen het gemiddelde berekenen
# in een dictionary opslaan
# in database opslaan

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

cur.execute("DELETE FROM temperatures_per_day")
conn.commit()

for i in temperature_per_day:
    cur.execute("INSERT INTO temperature_per_day VALUES (?,?)", (i, temperature_per_day[i]))

conn.commit()