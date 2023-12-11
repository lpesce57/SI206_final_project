import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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


#Adds data to the weather table
def add_weather_data(cur, conn):
    #Start date of 1,000 days ago, loops through 25 times each time the program is run, date is changed to reflect 25 days later
    start_date = datetime(2021, 3, 16)
    for i in range(25):
          current_date = start_date + timedelta(days=i)
          date = current_date.strftime("%Y-%d-%m")
          url = f"https://api.openweathermap.org/data/3.0/onecall/day_summary?lat=42.279594&lon=-83.732124&date={date}&tz=-05:00&appid={INSERT API KEY}"
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

#Creates a plot of the average temperature each day recorded
def plot_weather_data(database):
    conn = sqlite3.connect(database)
    cur = conn.cursor()

    cur.execute("SELECT date, high_temp, low_temp FROM weather")
    data = cur.fetchall()
    
    daily_average = {}
    
	#Goes through data from the database and places it into a dictionary
    for date, high_temp, low_temp in data:
        #Finds the mean of the daily high/low
        average_temp = (high_temp + low_temp) / 2
        #Adds the daily average to the dictionary
        daily_average[date] = average_temp

	#Dates is the keys and temperature is the values
    dates = list(daily_average.keys())
    temp = list(daily_average.values())

	#Plots the average temperatures by date
    plt.plot(dates, temp, label="Average Temperature")

    plt.xlabel("Date")
    plt.ylabel("Temperature")
    plt.title("Daily Average Temperature")
    plt.legend()
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    plt.show()
    print("SUCCESS")
    


#Executes all of the functions
def main():
    cur, conn = setUpDatabase('open_weather.db')
    create_weather_table(cur, conn)
    add_weather_data(cur, conn)
    plot_weather_data('open_weather.db')
    conn.close()

if __name__ == "__main__":
    main()
