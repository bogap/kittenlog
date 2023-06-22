from KinoPoiskAPI.kinopoisk_api import KP
from dotenv import dotenv_values


class Kinopoisk:
    def __init__(self):
        self.env_variables = dotenv_values(".env")
        self.kinopoisk = KP(token=self.env_variables["KINOPOISK_API_KEY"])

    def search(self, keyword):
        search = self.kinopoisk.search(keyword)

        for i in range(min(len(search), 5)):
            item = search[i]
            print("Название: " + item.ru_name,
                  "Оценка: " + str(item.kp_rate),
                  "Год выпуска: " + item.year,
                  "Страны: " + ", ".join(item.countries),
                  "Жанры: " + ", ".join(item.genres),
                  "Ссылка на фильм на кинопоиске: " + item.kp_url,
                  "Ссылка на постер фильма: " + item.poster,
                  sep="\n")
            print()


# # Пример использования
#
# kinop = Kinopoisk()
# keywords = input('>: ')
# kinop.search(keywords)
