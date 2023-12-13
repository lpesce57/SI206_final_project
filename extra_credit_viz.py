    
def extra_credit_viz(database):
    import sqlite3
    import pandas as pd
    import matplotlib.pyplot as plt

    
    conn = sqlite3.connect(database)

    df = pd.read_sql_query("SELECT rating, duration FROM omdb", conn)

    conn.close()

    df['duration'] = pd.to_numeric(df['duration'], errors='coerce')

    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

    plt.figure(figsize=(10, 8))
    plt.scatter(df['duration'], df['rating'])
    plt.xlabel("Duration")
    plt.ylabel("Rating")
    plt.title("Correlation Between Duration and Rating")
    plt.show()

extra_credit_viz('final_project (4).db')