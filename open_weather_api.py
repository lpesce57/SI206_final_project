import sqlite3
import requests
from datetime import datetime, timedelta

#Sets up the database that will read from Open Weather 
def setUpDatabase(database):
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    return cur, conn

#Creates a weather data table with UTC, date, high temperature and low temperature
def create_weather_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS weather (date TEXT PRIMARY KEY, high_temp REAL, low_temp REAL)")
    conn.commit()

#Used to check whether or not a date is already in the database
def date_in_database(cur, date):
    cur.execute("SELECT date FROM weather WHERE date=?", (date,))
    return cur.fetchone() is not None

#Adds data to the weather table
def add_weather_data(cur, conn):
    #Start date of 1,000 days ago, loops through 25 times each time the program is run, date is changed to reflect 25 days later
    start_date = datetime(2021, 3, 16)
    for i in range(25):
        #Check if the date is already in the database, uses the first date that is not
        while date_in_database(cur, start_date):
            current_date += timedelta(days=1)
            date = current_date.strftime("%Y-%m-%d")
        url = f"https://api.openweathermap.org/data/3.0/onecall/day_summary?lat=42.279594&lon=-83.732124&date={date}&tz=-05:00&appid={INSERT_KEY}"
        response = requests.get(url)
        data = response.json()
        #Checks the error code and then records the high/low temperatures
        if data.get("cod") != "404":
            temp_data = data.get("temperature", {})
            high_temp = temp_data.get("max", 0)
            low_temp = temp_data.get("min", 0)
            #Places all data into the database
            cur.execute("INSERT OR IGNORE INTO weather (date, high_temp, low_temp) VALUES(?, ?, ?)", (date, high_temp, low_temp))
    conn.commit()

#Executes all of the functions
def main():
    cur, conn = setUpDatabase('open_weather.db')
    create_weather_table(cur, conn)
    add_weather_data(cur, conn)
    conn.close()

if __name__ == "__main__":
    main()
