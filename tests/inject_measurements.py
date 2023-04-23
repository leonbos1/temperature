import requests
import json
import time
import datetime
import sqlite3
import random

def inject_daily():
    """
    Injects daily measurements into database
    """
    conn = sqlite3.connect('../backend/data.db')
    c = conn.cursor()

    current_time = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    for i in range(1440):
        current_time += datetime.timedelta(minutes=1)
        current_time_str = current_time.strftime("%H:%M:%S")
        current_date_str = current_time.strftime("%d-%m-%Y")

        #insert random values into database
        temp = round(20 + 10 * (i % 2), 2)
        humidity = round(50 + 10 * (i % 2), 2)
        c.execute("INSERT INTO measurements (degrees, humidity, date, time, sensor_id) VALUES (?, ?, ?, ?, ?)", (temp, humidity, current_date_str, current_time_str, 1))

        print("Inserted values: " + str(temp) + " " + str(humidity) + " " + current_date_str + " " + current_time_str)

    conn.commit()
    conn.close()
    print("Done inserting daily measurements")

def inject_monthly():
    """
    Injects monthly measurements into database
    makes a measurement for every 15 minutes for 30 days
    """
    conn = sqlite3.connect('../backend/data.db')
    c = conn.cursor()

    current_time = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    current_time -= datetime.timedelta(days=30)

    for i in range(2880):
        current_time += datetime.timedelta(minutes=15)
        current_time_str = current_time.strftime("%H:%M:%S")
        current_date_str = current_time.strftime("%d-%m-%Y")

        #insert random values into database
        temp = round(random.randint(20, 30), 2)
        humidity = round(random.randint(40, 60), 2)
        c.execute("INSERT INTO measurements (degrees, humidity, date, time, sensor_id) VALUES (?, ?, ?, ?, ?)", (temp, humidity, current_date_str, current_time_str, 1))

        print("Inserted values: " + str(temp) + " " + str(humidity) + " " + current_date_str + " " + current_time_str)
    
    conn.commit()
    conn.close()

def inject_yearly():
    """	
    Injects yearly measurements into database
    makes a measurement for every hour for 365 days
    """
    conn = sqlite3.connect('../backend/data.db')
    c = conn.cursor()

    current_time = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    current_time -= datetime.timedelta(days=365)

    for i in range(8760):
        current_time += datetime.timedelta(hours=1)
        current_time_str = current_time.strftime("%H:%M:%S")
        current_date_str = current_time.strftime("%d-%m-%Y")

        #insert random values into database
        temp = round(random.randint(20, 30), 2)
        humidity = round(random.randint(40, 60), 2)
        c.execute("INSERT INTO measurements (degrees, humidity, date, time, sensor_id) VALUES (?, ?, ?, ?, ?)", (temp, humidity, current_date_str, current_time_str, 1))

        print("Inserted values: " + str(temp) + " " + str(humidity) + " " + current_date_str + " " + current_time_str)
    
    conn.commit()
    conn.close()

def empty_db():
    """
    Empties the database
    """
    conn = sqlite3.connect('../backend/data.db')
    c = conn.cursor()
    c.execute("DELETE FROM measurements")
    conn.commit()
    conn.close()
    print("Done emptying database")
        
if __name__ == "__main__":
    inject_yearly()