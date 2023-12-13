import requests
import sqlite3

#Sets up the database that will read from IMDB
def setUpDatabase(database):
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    return cur, conn

#Creates a movie data table with id, title, year, rating, and duration
def create_movies_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS movies (id TEXT PRIMARY KEY, title TEXT, year INTEGER, rating REAL, duration INTEGER)")
    conn.commit()

#Used to check whether or not a movie is already in the database
def movie_in_database(cur, movie):
    cur.execute("SELECT id FROM movies WHERE id=?", (movie,))
    return cur.fetchone() is not None

#Adds data from IMDB to the database
def get_movie_data(cur, conn):
    url = "https://imdb-api.com/en/API/Top250Movies/k_twxmpxoq"
    response = requests.get(url)
    movie_data = response.json()

    #Starts at the top movie
    start_movie = 0

    #Check if the movie is already in the database, if it is move one movie down the list
    while movie_in_database(cur, start_movie):
        start_movie += 1

    #Gets the movie data from the first movie not in the database and the next 25 movies after
    data = movie_data["items"][start_movie:start_movie + 25]

    #Gets the title, year, rating and movie id for each movie
    for diction in data:
        title = diction["title"]
        year = diction["year"]
        #Turns rating into a float to assure it is documented correctly
        rating = float(diction["imDbRating"])
        id_num = diction["id"]

        #Gets a new URL based on the movie id to determine the movie duration
        data_url = f"https://imdb-api.com/en/API/Title/k_twxmpxoq/{id_num}"
        response2 = requests.get(data_url)
        movie_data2 = response2.json()
        duration = movie_data2["runtimeMins"]

        #Places the data into the table
        cur.execute("INSERT OR IGNORE INTO movies (id, title, year, rating, duration) VALUES(?, ?, ?, ?, ?)", (id_num, title, year, rating, duration))
    conn.commit()

#Writes to a text file
def compute_average_rating(cur):
    #Retrieve all ratings from the database
    cur.execute("SELECT rating FROM movies")
    ratings = cur.fetchall()
 
    #Calculate the average rating
    total_ratings = sum(rating[0] for rating in ratings)
    average_rating = total_ratings / len(ratings)

    #Write the average rating to average_rating.txt
    file_path = os.path.join(os.path.dirname(__file__), 'average_rating.txt')
    with open(file_path, 'w') as file:
        file.write(f'Average Rating: {average_rating}')

    print(f'Average Rating: {average_rating}')

#Executes all of the functions
def main():
    cur, conn = setUpDatabase('final_project.db')
    create_movies_table(cur, conn)
    get_movie_data(cur, conn)
    compute_average_rating(cur)
    conn.close()

if __name__ == "__main__":
    main()
