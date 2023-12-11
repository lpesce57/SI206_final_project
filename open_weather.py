import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

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
        kelvin_temp = (high_temp + low_temp) / 2
        average_temp = (kelvin_temp - 273.15) * 9/5 + 32
        #Adds the daily average to the dictionary
        daily_average[date] = average_temp

	#Dates is the keys and temperature is the values
    dates = list(daily_average.keys())
    temp = list(daily_average.values())

	#Plots the average temperatures by date
    plt.plot(dates, temp)
    plt.title("Average Temperature for 1,000 Days")
    plt.xlabel("Temperature")
    plt.ylabel("Date")
    plt.show()
    

def main():
    plot_weather_data('final_project.db')

if __name__ == "__main__":
    main()
