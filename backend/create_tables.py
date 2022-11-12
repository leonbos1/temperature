import sqlite3

conn = sqlite3.connect('data.db')
cur = conn.cursor()

#create new table with the average temperature per day
cur.execute("CREATE TABLE IF NOT EXISTS average_temperatures (id TEXT, degrees REAL)")
conn.commit()