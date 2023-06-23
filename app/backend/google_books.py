from requests import get
import json

API_KEY = "AIzaSyDBAFxQBMQ1Kovq62NpmGhW0mIuJSP0hH4"


class Book:
    """
    Class for google books api.
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
        return self.title

    def get_authors(self) -> list[str]:
        return self.authors

    def __len__(self) -> int:
        """
        Override len function.
        :return: number of pages.
        """
        return self.page_count


def get_book(request: str) -> list[Book] | None:
    """
    Get list of books by request.
    :param request: str request for google books api.
    :return: list of books class.
    """
    books = []
    try:
        response = get("https://www.googleapis.com/books/v1/volumes?q={}&key={}".format(request, API_KEY))
    except Exception as e:
        print("Что-то поломалосб у гугла ඞ\n", e)
        return None
    json_obj = json.loads(response.content)
    books_json = json_obj["items"]
    for book_instance in books_json:
        book_instance_volume_info = book_instance["volumeInfo"]

        title = book_instance_volume_info.get("title")
        subtitle = book_instance_volume_info.get("subtitle")
        authors = book_instance_volume_info.get("authors")
        publisher = book_instance_volume_info.get("publisher")
        published_date = book_instance_volume_info.get("publishedDate")
        page_count = book_instance_volume_info.get("pageCount")
        print_type = book_instance_volume_info.get("printType")
        categories = book_instance_volume_info.get("categories")
        image_links = book_instance_volume_info.get("imageLinks")
        if image_links:
            image_link_thumbnail = image_links.get("thumbnail")
        else:
            image_link_thumbnail = None
        language = book_instance_volume_info.get("language")
        description = book_instance_volume_info.get("description")
        preview_link = book_instance_volume_info.get("previewLink")
        canonical_link = book_instance_volume_info.get("canonicalVolumeLink")

        book = Book(title, subtitle, authors, publisher, published_date, page_count, print_type, categories,
                    image_link_thumbnail, language, description, preview_link, canonical_link)
        books.append(book)
    return books
