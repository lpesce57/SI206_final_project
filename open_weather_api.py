import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import requests
from datetime import datetime

#Sets up the database that will read from Open Weather 
def setUpDatabase(database):
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    return cur, conn

#Creates a weather data table with UTC, date, high temperature and low temperature
def create_weather_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS weather (utc INTEGER PRIMARY KEY, date TEXT, high_temp REAL, low_temp REAL)")
    conn.commit()


#Adds data to the weather table
def add_weather_data(cur, conn):
    #URL to access Open Weathers data in Ann Arbor
    url = "https://history.openweathermap.org/data/2.5/history/city?lat=42.279594&lon=-83.732124&type=hour&start=439788694&end=1702074636&appid=(API KEY)"
    response = requests.get(url)
    data = response.json()
    
	#Checks the error code and then creates weather_data to store data from the API, looks specifically at "list" section
    if data.get("cod") != "404":
        weather_data = data.get("list", [])

		#Goes through and records all the data we are searching for
        for weather in weather_data:
            #Within the list, accesses data in the main category
            main_data = weather.get("main", {})
            #Finds the high and low temperatures of the day
            high_temp = main_data.get("temp_max", 0)
            low_temp = main_data.get("temp_min", 0)
            #Gets the UTC
            utc = weather.get("dt", 0)
            #Converts the UTC to a date formatted as "December 23, 2023"
            utc_datetime = datetime.utcfromtimestamp(utc)
            date = utc_datetime.strftime("%B %d, %Y")
            #Places all data into the database
            cur.execute("INSERT OR IGNORE INTO weather (utc, date, high_temp, low_temp) VALUES(?, ?, ?, ?)", (utc, date, high_temp, low_temp))

        conn.commit()


#Creates a plot of the average temperature each day recorded
def plot_weather_data(database):
    conn = sqlite3.connect(database)
    cur = conn.cursor()

    cur.execute("SELECT utc, high_temp, low_temp FROM weather")
    data = cur.fetchall()
    
    daily_average = {}
    
	#Goes through data from the database and places it into a dictionary
    for utc, high_temp, low_temp in data:
        #Gets the current date
        curr_date = datetime.strptime(utc, "%B %d, %Y").date()
        #Finds the mean of the daily high/low
        average_temp = (high_temp + low_temp) / 2
        #Adds the daily average to the dictionary
        daily_average[curr_date] = average_temp

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
    


#Executes all of the functions
def main():
    cur, conn = setUpDatabase('open_weather.db')
    create_weather_table(cur, conn)
    add_weather_data(cur, conn)
    plot_weather_data('open_weather.db')
    conn.close()

if __name__ == "__main__":
    main()
