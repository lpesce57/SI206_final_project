import sqlite3
import matplotlib.pyplot as plt
import requests
from datetime import datetime

def setUpDatabase(db_name):
	api_key = "INSERT"
	base_url = "http://api.openweathermap.org/data/2.5/weather?"
	city_name = "Ann+Arbor"
	complete_url = f"{base_url}q={city_name}&appid={api_key}"
	conn = sqlite3.connect("/Users/laurenpesce/Desktop/SI\ 206\ Final\ Project/open_weather.db")
	cur = conn.cursor()
	return cur, conn, complete_url


def create_weather_db(cur, conn):
	cur.execute("CREATE TABLE IF NOT EXISTS weather (temp INTEGER PRIMARY KEY, month INTEGER, day INTEGER, year INTEGER)")
	conn.commit()
	
def add_weather_data(cur, conn, complete_url):
	response = requests.get(complete_url)
	weather_data = response.json()
	if weather_data["cod"] != "404":
		main_key = weather_data["main"]
		temp = main_key["temp"]["max"]
		date = datetime.utcfromtimestamp(weather_data["dt"]).strftime('%Y-%m-%d')
		month, day, year = map(int, date.split('-'))
		cur.execute("INSERT OR IGNORE INTO weather (temp, month, date, year) VALUES(?, ?, ?, ?)", (temp, month, day, year))
		conn.commit()
	conn.close()
	

def main():
    # SETUP DATABASE AND TABLE
	cur, conn = setUpDatabase('open_weather.db')
	create_weather_db(cur, conn)
	api_key = "INSERT"
	base_url = "http://api.openweathermap.org/data/2.5/weather?"
	city_name = "Ann+Arbor"
	complete_url = f"{base_url}q={city_name}&appid={api_key}"
	add_weather_data(cur, conn, complete_url)


if __name__ == "__main__":
    main()
	
