import sqlite3
from omdbapi.movie_search import GetMovie
from datetime import datetime
import os

#Sets up the database that will read from OMDB
def setUpDatabase(database):
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    return cur, conn

#Makes a list of all the movies collected from IMDB API
def get_movie_data(database):
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute("SELECT title FROM movies")
    data = cur.fetchall()
    titles = []
    #Adds all movie titles to a list
    for title in data:
        titles.append(title)

    return titles

#Convert the release date to be correctly structured: 20021223
def convert_date(date):
    converted_date = datetime.strptime(date, "%d %b %Y")
    formatted_date = converted_date.strftime("%Y%m%d")

    return int(formatted_date)


#Creates a OMDB data table with date, title, rating, and duration
def create_movies_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS omdb (date INTEGER PRIMARY KEY, title TEXT, rating REAL, duration INTEGER)")
    conn.commit()

#Creates a rated table for movie ratings (PG-13)
def create_rated_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS rated (date INTEGER PRIMARY KEY, rated TEXT)")
    conn.commit()

#Used to check whether or not a movie is already in the database
def movie_in_database(cur, movie):
    cur.execute("SELECT id FROM movies WHERE id=?", (movie,))
    return cur.fetchone() is not None

#Used to check whether or not a date is already in the database
def date_in_database(cur, date):
    cur.execute("SELECT date FROM omdb WHERE date=?", (date,))
    return cur.fetchone() is not None

#Adds data from IMDB to the database
def get_omdb_data(cur, conn, titles):
    #Starts at index 0
    index = 0

    #Check if the movie is already in the database, if it is move one movie down the list
    while movie_in_database(cur, index):
        index += 1
   
    #Gets the movie data from the first movie not in the database and the next 25 movies after
    data = titles[index:index + 25]
    movie = GetMovie(api_key='832447e3')   
    #Gets the title, year, rating and movie id for each movie
    for title_name in data:
        curr_title = movie.get_movie(title = title_name)
        #Gets the title from the curr_title dict
        str_title = str(curr_title["title"])

        #Gets the release date from the curr_title dict and converts it to correct format
        release_date = str(curr_title["released"])
        date = convert_date(release_date)
        #Gets the imdb rating from the curr_title dict and converts it to float
        imdb_rating = float(curr_title["imdbrating"])
        #Gets the duration from the curr_title dict and converts it to only the integer
        duration = curr_title["runtime"]
        minutes = int(duration.split()[0])

        #Places the data into the table
        cur.execute("INSERT OR IGNORE INTO omdb (date, title, rating, duration) VALUES(?, ?, ?, ?)", (date, str_title, imdb_rating, minutes))
    conn.commit()

#Adds data about movie rating (PG-13) from OMDB to the database
def get_rated_data(cur, conn, date_titles):
   #Starts at index 0
    index = 0

    #Check if the movie is already in the database, if it is move one movie down the list
    while movie_in_database(cur, index):
        index += 1
   
    #Gets the movie data from the first movie not in the database and the next 25 movies after
    data = date_titles[index:index + 25]
    movie = GetMovie(api_key='832447e3')
    #Gets the title, year, rating and movie id for each movie
    for title_name in data:
        curr_title = movie.get_movie(title = title_name)
        #Gets the release date and correctly formats it
        release_date = str(curr_title["released"])
        date = convert_date(release_date)
        #Gets the rating from the curr_title dict
        rating = curr_title["rated"]

        #Places the data into the table
        cur.execute("INSERT OR IGNORE INTO rated (date, rated) VALUES(?, ?)", (date, rating))
    conn.commit()

def compute_average_omdb_rating(cur):
    # Retrieve all ratings from the database
    cur.execute("SELECT rating FROM omdb")
    ratings = cur.fetchall()

    # Calculate the average rating
    total_ratings = sum(rating[0] for rating in ratings)
    average_rating = total_ratings / len(ratings)

    # Write the average rating to a text file
    file_path = os.path.join(os.path.dirname(__file__), 'average_omdb_rating.txt')
    with open(file_path, 'w') as file:
        file.write(f'Average Rating: {average_rating}')

    print(f'Average Rating: {average_rating}')

# Executes all of the functions
def main():
    cur, conn = setUpDatabase('final_project.db')
    create_movies_table(cur, conn)
    movie_titles = get_movie_data('final_project.db')
    get_omdb_data(cur, conn, movie_titles)
    create_rated_table(cur, conn)
    get_rated_data(cur, conn, movie_titles)
    compute_average_omdb_rating(cur)
    conn.close()

if __name__ == "__main__":
    main()