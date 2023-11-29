import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt
import rottentomatoes as rt

print(rt.tomatometer("happy gilmore"))
# Output: 61
# Type: int

print(rt.audience_score('top gun maverick'))
# Output: 99
# Type: int

print(rt.rating('everything everywhere all at once'))
# Output: R
# Type: str

print(rt.genres('top gun'))
# Output: ['Action', 'Adventure']
# Type: list[str]

print(rt.weighted_score('happy gilmore'))
# Output: 69
# Type: int

print(rt.year_released('happy gilmore'))
# Output: 1996
# Type: str

print(rt.actors('top gun maverick', max_actors=5))
# Output: ['Tom Cruise', 'Miles Teller', 'Jennifer Connelly', 'Jon Hamm', 'Glen Powell']
# Type: list[str]

# --- Using the Movie class ---
movie = rt.Movie('top gun')
print(movie)
# Output
    # Top Gun, PG, 1h 49m.
    # Released in 1986.
    # Tomatometer: 58
    # Weighted score: 66
    # Audience Score: 83
    # Genres - ['Action', 'Adventure']
    # Prominent actors: Tom Cruise, Kelly McGillis, Anthony Edwards, Val Kilmer, Tom Skerritt.
# Type: str

print(movie.weighted_score)
# Output: 66
# Type: int
