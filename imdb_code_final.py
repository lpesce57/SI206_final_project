import requests 
import json

def get_movie_data():
   
    url = "https://imdb-api.com/en/API/InTheaters/k_twxmpxoq"
    movies = {}
    response = requests.get(url)
    movie_data = response.json()

    data = movie_data["items"]
    for diction in data:
        listed = []
        title = diction["title"]
        rating = diction["imDbRating"]
        critic = diction["metacriticRating"]
        release_date = diction["releaseState"]
        splitted = release_date.split()
        month = splitted[1]
        if month == "Nov":
            month2 = "11"
        if month == "Dec":
            month2 = "12"
        if month == "Mar":
            month2 = "03"   
        if month == "Sep":
            month2 == "09"
        if month == "Oct":
            month2 = "10"
        if month == "Jun":
            month2 = "06"
        if month == "Jul":
            month2 = "07"
        if month == "Feb":
            month2 = "02"
        if month== "Apr":
            month2 = "04"
        if month == "May":
            month2 = "05"
        if month == "Aug":
            month2 = "08"
        if month == "Jan":
            month2 = "01"
        newyear = splitted[2]+"-"+ month2 + "-"+ splitted[0]
        duration = diction["runtimeMins"]
        movies[title] = newyear, rating, duration
       
    return movies

def get_movie_data2():
    listed1 = ["2014", "2013","2015", "2016", "2017", "2018","2019","2020","2021", "2022", "2023"]
    url = "https://imdb-api.com/en/API/Top250Movies/k_twxmpxoq"
    movies = {}
    response = requests.get(url)
    movie_data = response.json()
    
    data = movie_data["items"]
    for diction in data:
        listed = []
        title = diction["title"]
        year = diction["year"]
        year = str(year)
        rating = diction["imDbRating"]
        id_num = diction["id"]
        
        data_url = f"https://imdb-api.com/en/API/Title/k_twxmpxoq/{id_num}"
        
        response2 = requests.get(data_url)
        movie_data2 = response2.json()
        duration = movie_data2["runtimeMins"]
        date = movie_data2["releaseDate"]
        
        if year in listed1:
            movies[title] = date, rating, duration
    return movies

movies = get_movie_data()
movies2 = get_movie_data2()

def plot_movie_data(movies, movies2):
    import sqlite3

    conn = sqlite3.connect('final_project (1).db')  
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Top_Movies2(movie, date, fan_rating, duration)''')
    
    conn.commit()

    for key, value in movies.items():
        movie = key
        newyear, rating, duration = value
        c.execute('''INSERT INTO Top_Movies2(movie, date, fan_rating, duration)
              VALUES(?,?,?,?)''', (movie, newyear, rating, duration))
    for key, value in movies2.items():
        movie = key
        newyear, rating, duration = value
        c.execute('''INSERT INTO Top_Movies2(movie, date, fan_rating, duration)
              VALUES(?,?,?,?)''', (movie, newyear, rating, duration))
    conn.commit() 
    conn.close()  
    
