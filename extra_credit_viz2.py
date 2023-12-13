    
def extra_credit_viz2(database):
    import sqlite3
    import pandas as pd
    import matplotlib.pyplot as plt


    conn = sqlite3.connect(database)

    df = pd.read_sql_query("SELECT date, duration FROM omdb", conn)

    conn.close()

# Convert date to datetime format, if it's not
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')

# Convert rating to numeric values, if it's not
    df['duration'] = pd.to_numeric(df['duration'], errors='coerce')


    df = df.sort_values('date')


    plt.figure(figsize=(10, 8))
    plt.plot(df['date'], df['duration'], '-o')
    plt.xlabel("Date")
    plt.ylabel("duration")
    plt.title("Duration Over Time")
    plt.show()
extra_credit_viz2('final_project (4).db')