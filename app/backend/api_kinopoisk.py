from KinoPoiskAPI.kinopoisk_api import KP


class Kinopoisk:
    """
    The Kinopoisk class provides a simple interface to search for movies using the Kinopoisk API.

    Attributes:
        kinopoisk (KP): An instance of the KP class from the KinoPoiskAPI module.

    Methods:
        search(keyword): Searches for movies based on the provided keyword and returns information about the top 5 matches.
    """

    def __init__(self):
        """
        Initializes a new instance of the Kinopoisk class.

        It sets the API key for Kinopoisk website and initializes the KP class from the KinoPoiskAPI module.
        """
        self.api_key = '409e9761-5a60-444a-964a-98372b936ed0'
        self.kinopoisk = KP(token=self.api_key)

    def search(self, keyword):
        """
        Searches for movies based on the provided keyword and returns information about the top 5 matches.

        Args:
            keyword (str): The keyword to search for movies.

        Returns:
            list: A list of dictionaries containing information about the top 5 movie matches.
                Each dictionary contains the following keys:
                - "title" (str): The movie's title in Russian.
                - "rating" (str): The movie's rating on Kinopoisk.
                - "release year" (int): The year the movie was released.
                - "countries" (str): A comma-separated string of the movie's countries.
                - "genres" (str): A comma-separated string of the movie's genres.
                - "link to movie on kinopoisk" (str): The URL of the movie on Kinopoisk.
                - "link to poster" (str): The URL of the movie's poster.

        """
        search = self.kinopoisk.search(keyword)
        list_of_movies = []

        for i in range(min(len(search), 5)):
            item = search[i]
            info = {
                "title": item.ru_name,
                "rating": str(item.kp_rate),
                "release year": item.year,
                "countries": ", ".join(item.countries),
                "genres": ", ".join(item.genres),
                "link to movie on kinopoisk": item.kp_url,
                "link to poster": item.poster
            }
            list_of_movies.append(info)
        return list_of_movies
