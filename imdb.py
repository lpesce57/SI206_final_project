import sqlite3
import matplotlib.pyplot as plt

#Plots the movie data
def plot_movie_data(database):
    conn = sqlite3.connect(database)
    cur = conn.cursor()

    cur.execute("SELECT id, title, year, rating, duration FROM movies")
    data = cur.fetchall()
    top_movies = {}

    for key, value in data:
        #Finds all of the data we are seeking
        movie = key
        released_year, rating, duration = value
        #Puts in data based on movie
        top_movies[movie] = released_year, rating, duration

        #Create matlabplot accordingly
       

def main():
    plot_movie_data('final_project.db')

if __name__ == "__main__":
    main()
