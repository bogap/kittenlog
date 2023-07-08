from KinoPoiskAPI.kinopoisk_api import KP
from dotenv import dotenv_values


class Kinopoisk:
    def __init__(self):
        self.env_variables = dotenv_values(".env")
        self.kinopoisk = KP(token='409e9761-5a60-444a-964a-98372b936ed0')

    def search(self, keyword):
        search = self.kinopoisk.search(keyword)
        list_of_movies = []

        for i in range(min(len(search), 5)):
            item = search[i]
            info = {"Название": item.ru_name,
                  "Оценка": str(item.kp_rate),
                  "Год выпуска": item.year,
                  "Страны": ", ".join(item.countries),
                  "Жанры": ", ".join(item.genres),
                  "Ссылка на фильм на кинопоиске": item.kp_url,
                  "Ссылка на постер фильма": item.poster}
            list_of_movies.append(info)
        return list_of_movies

