import sqlite3

# alle data opslaan tot en met een maand geleden
# van alle dagen het gemiddelde berekenen
# in een dictionary opslaan
# in database opslaan

conn = sqlite3.connect('data.db')
cur = conn.cursor()
cur.execute("SELECT degrees, date, time FROM temperatures ORDER BY id DESC LIMIT 40500")

data = cur.fetchall()

for i in data:
    print(i)