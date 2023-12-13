import sqlite3
import rottentomatoes as rt
import os

#Sets up the database that will read from rotten tomatoes
def setUpDatabase(database):
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    return cur, conn

#Makes a list of all the movies in the database
def get_movie_data(database):
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute("SELECT title FROM movies")
    data = cur.fetchall()
    titles = []

    #Goes through all the tiles in the database and adds them to the titles list
    for title in data:
        titles.append(title)

    return titles

#Creates a rotten tomatoes data table with title, tomato meter and audience score
def create_movies_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS rotten_tomatoes (title TEXT PRIMARY KEY, tomato_meter TEXT, audience_score TEXT)")
    conn.commit()

#Used to check whether or not a movie is already in the database
def movie_in_database(cur, movie):
    cur.execute("SELECT title FROM rotten_tomatoes WHERE title=?", (movie,))
    return cur.fetchone() is not None

#Adds data from rotten tomatoes to the database
def get_rt_data(cur, conn, titles):
    #Starts at index 0
    index = 0

    #Check if the movie is already in the database, if it is move one movie down the list
    while movie_in_database(cur, index):
        index += 1

    #Gets the movie data from the first movie not in the database and the next 25 movies after
    data = titles[index:index + 25]

    #Gets the title, tomato meter, and audience score for each movie
    for title in data:
        tomato_meter = rt.tomatometer(title[index])
        audience_score = rt.audience_score(title[index])
        movie_title = title[index]

        #Places the data into the table
        cur.execute("INSERT OR IGNORE INTO rotten_tomatoes (title, tomato_meter, audience_score) VALUES(?, ?, ?)", (movie_title, tomato_meter, audience_score))
    conn.commit()

def compute_average_rt_scores(cur):
    # Retrieve all scores from the database
    cur.execute("SELECT tomato_meter, audience_score FROM rotten_tomatoes")
    scores = cur.fetchall()

    # Calculate the average scores
    total_tomato_meter = sum(int(score[0]) for score in scores if score[0].isdigit())
    total_audience_score = sum(int(score[1]) for score in scores if score[1].isdigit())

    average_tomato_meter = total_tomato_meter / len(scores)
    average_audience_score = total_audience_score / len(scores)

    # Write the average scores to a text file
    file_path = os.path.join(os.path.dirname(__file__), 'average_rt_scores.txt')
    with open(file_path, 'w') as file:
        file.write(f'Average Tomato Meter: {average_tomato_meter}\n')
        file.write(f'Average Audience Score: {average_audience_score}')

    print(f'Average Tomato Meter: {average_tomato_meter}')
    print(f'Average Audience Score: {average_audience_score}')

# Executes all of the functions
def main():
    cur, conn = setUpDatabase('final_project.db')
    create_movies_table(cur, conn)
    movie_titles = get_movie_data('final_project.db')
    get_rt_data(cur, conn, movie_titles)
    compute_average_rt_scores(cur)
    conn.close()

if __name__ == "__main__":
    main()