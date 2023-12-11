import requests 
import json
import sqlite3

def get_movie_data():
   
    url = "https://imdb-api.com/en/API/Top250Movies/k_twxmpxoq"
    movies = {}
    response = requests.get(url)
    movie_data = response.json()

    data = movie_data["items"]
    for diction in data[:100]:
        listed = []
        title = diction["title"]
        year = diction["year"]
        rating = diction["imDbRating"]
        id_num = diction["id"]
        
        data_url = f"https://imdb-api.com/en/API/Title/k_twxmpxoq/{id_num}"
        response2 = requests.get(data_url)
        movie_data2 = response2.json()
        duration = movie_data2["runtimeMins"]
        
        movies[title] = year, rating, duration
       
    return movies

def plot_movie_data(movies):
    conn = sqlite3.connect('final_project.db')  
    c = conn.cursor()
    c.execute('''CREATE TABLE Top_Movies(movie, year, rating, duration)''')
    conn.commit()

    for key, value in movies.items():
        movie = key
        released_year, rating, duration = value
        c.execute('''INSERT INTO Top_Movies(movie, year, rating, duration)
              VALUES(?,?,?,?)''', (movie, released_year, rating, duration))

    conn.commit() 
    conn.close() 
    