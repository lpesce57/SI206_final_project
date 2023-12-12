def tmdb_data(database):
    import sqlite3
    import requests

    # Your TMDb API key
    api_key = "73a6e60f04efa445f894f0605f9f095c"
    base_url = "https://api.themoviedb.org/3/search/movie"
    table_name = "movies"

    # Connect to your database
    conn = sqlite3.connect(database)
    c = conn.cursor()

    # Create 'rating' column if it doesn't exist
    c.execute(f"ALTER TABLE {database} ADD COLUMN rating REAL")

    # Fetches all titles, you could limit it to specific rows here
    titles = c.execute(f"SELECT title FROM {table_name}").fetchall()

    # Close connection after fetching titles
    conn.close()

    for i in range(0, len(titles), 25):
        single_set = titles[i:i+25]  # Select a set of 25 titles
        for title1 in single_set:
            params = {
                'api_key': api_key,
                'query': title1[0],
                'include_adult': False,
                'language': 'en-US',
                'page': 1,
            }

        # Make the request
            response = requests.get(base_url, params=params)

            if response.status_code == 200:
                results = response.json()
                for movie in results['results']:
                    if movie["title"] == title1[0]:
                        rating = movie['vote_average']
                        # Establish a connection to the database to insert the rating
                        conn = sqlite3.connect(database)
                        c = conn.cursor()
                        c.execute(f"UPDATE {table_name} SET rating = {rating} WHERE title = '{title1[0]}'")
                        conn.commit()
                        conn.close()
            else:
                print(f"Error: {response.status_code}")
                
tmdb_data('final_project.db')