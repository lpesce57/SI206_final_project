import sqlite3
import matplotlib.pyplot as plt
import requests
import json
from datetime import datetime

def setUpDatabase(database):
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    return cur, conn

def create_weather_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS weather (date TEXT PRIMARY KEY, high_temp REAL, low_temp REAL)")
    conn.commit()

def add_weather_data(cur, conn):
    ap_id = "INSERT"
    url = "https://history.openweathermap.org/data/2.5/history/city?lat=42.279594&lon=-83.732124&type=hour&start=439788694&end=1702074636&appid=(ap_id)"
    response = requests.get(url)
    weather_data = response.json()

    if weather_data["cod"] != "404":
        for data in weather_data:
            main_data = data["main"]
            high_temp = main_data["temp"]["max"]
            low_temp = main_data["temp"]["min"]
            date = datetime.utcfromtimestamp(data["dt"]).strftime('%Y-%m-%d')
            cur.execute("INSERT OR IGNORE INTO weather (date, high_temp, low_temp) VALUES(?, ?, ?)", (date, high_temp, low_temp))
        conn.commit()

def main():
    cur, conn = setUpDatabase('open_weather.db')
    create_weather_table(cur, conn)
    add_weather_data(cur, conn)
    conn.close()

if __name__ == "__main__":
    main()
