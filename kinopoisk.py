import json
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests

sns.set(font_scale=1.3, palette="Set2", style="whitegrid")

with open('token.txt') as token_file:
    token = token_file.read()

film_id = "1143242"

# Формируем путь для задания запроса
"""url="https://api.kinopoisk.dev/v1.3/movie/1143242"
url = "https://api.kinopoisk.dev/v1.3/movie?&limit=10&id={}/token/{}".format(
    film_id,
    token
)"""

#

def get_movie_info(movie_title):
    url = f"https://api.kinopoisk.cloud/movies?keyword={movie_title}&fields=id,name,year,countries,genres,description"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["total"] > 0:
            movie = data["movies"][0]
            print("Title:", movie["name"])
            print("Year:", movie["year"])
            print("Countries:", ", ".join(movie["countries"]))
            print("Genres:", ", ".join(movie["genres"]))
            print("Description:", movie["description"])
        else:
            print("No movie found.")
    else:
        print("Error:", response.status_code)


# Example usage
movie_title = input("Enter movie title: ")
get_movie_info(movie_title)
