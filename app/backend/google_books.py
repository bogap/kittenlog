import json

from requests import get
from requests.exceptions import RequestException

API_KEY = "AIzaSyDBAFxQBMQ1Kovq62NpmGhW0mIuJSP0hH4"


class Book:
    """
    Represents a book with various attributes.
    """

    def __init__(
            self,
            title: str,
            subtitle: str | None,
            authors: list[str],
            publisher: str | None,
            published_date: str | None,
            page_count: int | None,
            print_type: str | None,
            categories: list[str] | None,
            image_link_thumbnail: str | None,
            language: str | None,
            description: str | None,
            preview_link: str | None,
            canonical_link: str | None,
    ):
        """
        Initialize a Book object with the provided attributes.

        :param title: The title of the book.
        :param subtitle: The subtitle of the book (optional).
        :param authors: A list of authors of the book.
        :param publisher: The publisher of the book (optional).
        :param published_date: The published date of the book (optional).
        :param page_count: The number of pages in the book (optional).
        :param print_type: The print type of the book (optional).
        :param categories: A list of categories or genres the book belongs to (optional).
        :param image_link_thumbnail: The URL of the book's thumbnail image (optional).
        :param language: The language of the book (optional).
        :param description: The description or summary of the book (optional).
        :param preview_link: The URL for previewing the book (optional).
        :param canonical_link: The canonical URL of the book (optional).
        """
        self.title = title
        self.subtitle = subtitle
        self.authors = authors
        self.publisher = publisher
        self.published_date = published_date
        self.page_count = page_count
        self.print_type = print_type
        self.categories = categories
        self.image_link_thumbnail = image_link_thumbnail
        self.language = language
        self.description = description
        self.preview_link = preview_link
        self.canonical_link = canonical_link

    def get_title(self) -> str:
        """
        Get the title of the book.

        :return: The title of the book.
        """
        return self.title

    def get_authors(self) -> list[str]:
        """
        Get the list of authors of the book.

        :return: A list of authors of the book.
        """
        return self.authors

    def to_dict(self) -> dict[str, str | list[str] | int | None]:
        """
        Convert the Book object to a dict.

        :return: A dictionary of parameters of a book.
        """
        return {
            "title": self.title,
            "subtitle": self.subtitle,
            "authors": self.authors,
            "publisher": self.publisher,
            "published_date": self.published_date,
            "page_count": self.page_count,
            "print_type": self.print_type,
            "categories": self.categories,
            "image_link_thumbnail": self.image_link_thumbnail,
            "language": self.language,
            "description": self.description,
            "preview_link": self.preview_link,
            "canonical_link": self.canonical_link
        }

    def __len__(self) -> int:
        """
        Override the len() function to get the number of pages in the book.

        :return: The number of pages in the book.
        """
        return self.page_count


def get_book(request: str) -> list[dict[str, str | list[str] | int | None]] | None:
    """
    Get a list of books based on the provided request using the Google Books API.

    :param request: The request string for the Google Books API.
    :return: A list of dicts representing the books.
             Returns None if there was an error or no books were found.
    """
    books = []
    try:
        response = get(f"https://www.googleapis.com/books/v1/volumes?q={request}&key={API_KEY}")
    except RequestException as e:
        print("An error occurred while making the request to Google Books API:\n", e)
        return None
    json_obj = json.loads(response.content)
    book_instances_json = json_obj["items"]
    k = 0
    for book_instance_json in book_instances_json:
        if k <= 5:
            k += 1
            book_instance_volume_info = book_instance_json.get("volumeInfo", {})

            title = book_instance_volume_info.get("title")
            subtitle = book_instance_volume_info.get("subtitle")
            authors = book_instance_volume_info.get("authors", [])
            publisher = book_instance_volume_info.get("publisher")
            published_date = book_instance_volume_info.get("publishedDate")
            page_count = book_instance_volume_info.get("pageCount")
            print_type = book_instance_volume_info.get("printType")
            categories = book_instance_volume_info.get("categories")
            image_links_dict = book_instance_volume_info.get("imageLinks", {})
            image_link_thumbnail = image_links_dict.get("thumbnail")
            language = book_instance_volume_info.get("language")
            description = book_instance_volume_info.get("description")
            preview_link = book_instance_volume_info.get("previewLink")
            canonical_link = book_instance_volume_info.get("canonicalVolumeLink")

            book = Book(title, subtitle, authors, publisher, published_date, page_count, print_type, categories,
                        image_link_thumbnail, language, description, preview_link, canonical_link)
            books.append(book.to_dict())
    if not books:
        return None
    return books
