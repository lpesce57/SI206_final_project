import sqlite3
import requests
from datetime import datetime

#Sets up the database that will read from Open Weather 
def setUpDatabase(database):
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    return cur, conn

#Makes a list of all the dates of movies released in the omdb database
def get_dates(database):
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute("SELECT date FROM omdb")
    data = cur.fetchall()
    dates = []

    #Add all the dates to the date list
    for date in data:
        dates.append(date)

    return dates

#Used to check whether or not a date is already in the database
def date_in_database(cur, index):
    cur.execute("SELECT date FROM weather WHERE date=?", (index[0],))
    return cur.fetchone() is not None

#Creates a weather data table with date, high temperature and low temperature
def create_weather_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS weather (date INTEGER PRIMARY KEY, high_temp REAL, low_temp REAL)")
    conn.commit()

#Adds data to the weather table
def add_weather_data(cur, conn, dates):
    #Starts at index 0
    index = 0

    #Check if the date is already in the database, if it is move one date down the list
    while date_in_database(cur, dates[index]):
        index += 1

    #Gets the date data from the first date not in the database and the next 25 date after
    date_data = dates[index:index + 25]

    #Goes through all the dates in date_data
    for curr_date in date_data:
        #Changes the date format to be correctly formatted for the URL
        formatted_date = f"{str(curr_date[0])[:4]}-{str(curr_date[0])[4:6]}-{str(curr_date[0])[6:]}"

        url = f"https://api.openweathermap.org/data/3.0/onecall/day_summary?lat=42.279594&lon=-83.732124&date={formatted_date}&tz=-05:00&appid=(API_KEY)"
        response = requests.get(url)
        data = response.json()
        #Checks the error code and then records the high/low temperatures
        if data.get("cod") != "404":
            temp_data = data.get("temperature", {})
            high_temp = temp_data.get("max", 0)
            low_temp = temp_data.get("min", 0)
            #Places all data into the database
            cur.execute("INSERT OR IGNORE INTO weather (date, high_temp, low_temp) VALUES(?, ?, ?)", (int(curr_date[0]), high_temp, low_temp))
    conn.commit()

#Executes all of the functions
def main():
    cur, conn = setUpDatabase('final_project.db')
    create_weather_table(cur, conn)
    dates = get_dates('final_project.db')
    add_weather_data(cur, conn, dates)
    conn.close()

if __name__ == "__main__":
    main()
