import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt
import imdb


# creating an instance of the IMDB()
ia = imdb.IMDb()
# Using the Search movie method
items = ia.search_movie('Avengers')
for i in items:
	print(i)

