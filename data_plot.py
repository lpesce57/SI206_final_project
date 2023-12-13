import sqlite3
import matplotlib.pyplot as plt

#Sets up the database that will read from rotten tomatoes
def setUpDatabase(database):
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    return cur, conn

#Makes a list of all the movies in the database
def plot_weather(cur, conn, database):
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    movie_ratings = {}
    movie_weather = {}

    cur.execute("SELECT rotten_tomatoes.title, rotten_tomatoes.tomato_meter, rotten_tomatoes.audience_score, movies.rating FROM rotten_tomatoes JOIN movies ON rotten_tomatoes.title = movies.title")
    rating_data = cur.fetchall()

    for row in rating_data:
        title = row[0]
        tomato_meter = row[1]
        audience_score = row[2]
        imdb_rating = row[3] * 10
        #Convert Tomato Meter and Audience Score to a float
        float_tomato_meter = float(tomato_meter)
        if audience_score is not None:
            float_audience_score = float(audience_score)
        else:
            float_audience_score = 0

        avg = (float_tomato_meter + float_audience_score + float(imdb_rating)) / 3

        movie_ratings[title] = avg

    #Fetching movie/weather data from movies and weather tables
    cur.execute("SELECT omdb.title, weather.date, weather.high_temp, weather.low_temp FROM omdb JOIN weather ON omdb.date = weather.date")
    weather_data = cur.fetchall()

    titles = []
    ratings = []
    temperatures = []

    for row in weather_data:
        title = row[0]
        high_temp = row[2]
        low_temp = row[3]

        avg_temp = (high_temp + low_temp) / 2
        movie_weather[title] = avg_temp

    for title, rating in movie_ratings.items():
        # Skip movies without weather data
        if title in movie_weather:
            titles.append(title)
            ratings.append(rating)
            temperatures.append(movie_weather[title])

    plt.scatter(ratings, temperatures)
    plt.xlabel('Mean Rating of Rotten Tomatoes, Audience Score, and IMDB Ratings')
    plt.ylabel('Mean High and Low Temperature')
    plt.title('The Average Rating of Movies Based on Temperature in Ann Arbor on Release Date')
    plt.show()



#Create a plot to compare IMDB ratings, tomato meter and audience score
def plot_rating_differences(cur, conn, database):
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    #Get the tomato meter, audience score and title from rotten tomatoes
    cur.execute("SELECT title, tomato_meter, audience_score FROM rotten_tomatoes")
    data = cur.fetchall()
    rt = {}

    #Goes through Rotten Tomatoes to get their tomato meter and audience score
    for tomatoes in data:
        title = tomatoes[0]
        tomato_meter = tomatoes[1]
        audience_score = tomatoes[2]

        rt[title] = [tomato_meter, audience_score]

    #Get the title and IMDB rating from movies
    cur.execute("SELECT title, rating FROM movies")
    data = cur.fetchall()
    imdb_rates = {}

    #Goes through IMDB movies and gets their ratings
    for irs in data:
        title = irs[0]
        rate = irs[1]
        rate = rate * 10

        imdb_rates[title] = rate

    #Begins to compare the two types of scores
    scores_dict = {}
    for row in data:
        title_name = row[0]
        scores_dict[title_name] = [imdb_rates[title_name], rt[title_name]]

    for title_name, score_val in scores_dict.items():
        imdb_rating = score_val[0]
        rt_score = score_val[1][0]
    
        difference = imdb_rating - float(rt_score)
        plt.bar(title_name, difference)

    plt.xlabel('Movie Title')
    plt.ylabel('Ratings')
    plt.title('Difference in Rotten Tomato and IMDB Ratings')
    plt.xticks(rotation=90)
    plt.show()

# Plot the average score of the movies based on the type it rated
def plot_average_ratings_by_category(cur, conn, database):
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    movie_ratings = {}
    movie_categories = {}

    # Fetching movie ratings data from rotten_tomatoes table
    cur.execute("SELECT title, tomato_meter, audience_score FROM rotten_tomatoes")
    rating_data = cur.fetchall()

    # Get the average between all the movie ratings for every movie
    for row in rating_data:
        title = row[0]
        tomato_meter = row[1]
        audience_score = row[2]
        
        # Convert Tomato Meter and Audience Score to a float
        float_tomato_meter = float(tomato_meter)

        if audience_score is not None:
            float_audience_score = float(audience_score)
        else:
            float_audience_score = 0

        avg = (float_tomato_meter + float_audience_score) / 2

        movie_ratings[title] = avg

    # Fetching movie categories from rated table
    cur.execute("SELECT rated FROM rated")
    category_data = cur.fetchall()

    # Get the rating category for each movie
    for row in category_data:
        category = row[0]

        # Initialize possible categories
        possible_categories = ["PG", "PG-13", "R", "G"]

        # Check if the category is in possible_categories, otherwise assign "Other"
        if category not in possible_categories:
            category = "Other"

        if title in movie_ratings:
            if category not in movie_categories:
                movie_categories[category] = []

            movie_categories[category].append(movie_ratings[title])

    # Plotting to make a bar chart of ratings for each rating type
    rating_types = list(movie_categories.keys())
    average_ratings = [sum(ratings) / len(ratings) for ratings in movie_categories.values()]

    plt.bar(rating_types, average_ratings)
    plt.xlabel('Rating Type')
    plt.ylabel('Average Rating')
    plt.title('Average Rating for Each Rating Type')
    plt.show()


#Create all plots
def main():
    cur, conn = setUpDatabase('final_project.db')
    plot_rating_differences(cur, conn, 'final_project.db')
    plot_weather(cur, conn, 'final_project.db')
    plot_average_ratings_by_category(cur, conn, 'final_project.db')
    

if __name__ == "__main__":
    main()

