import requests

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel


class URLView(QWidget):
    """
    URLView class represents a widget for displaying an image from a given URL.

    Attributes:
        urlEdit (QLineEdit): A QLineEdit widget to display the URL of the image.
        imageLabel (QLabel): A QLabel widget to display the image.
    """

    def __init__(self, url, parent=None):
        """
        Initializes an instance of the URLView class.

        Args:
            url (str): The URL of the image to display.
            parent (QWidget): The parent widget. Default is None.
        """

        super().__init__(parent)
        layout = QVBoxLayout(self)

        self.urlEdit = QLineEdit()
        self.urlEdit.setText(url)

        self.imageLabel = QLabel()
        self.imageLabel.setScaledContents(True)
        layout.addWidget(self.imageLabel)

        self._load_image_from_url()

    def _load_image_from_url(self):
        """
        Loads the image data from the specified URL and sets it in the imageLabel widget.
        """

        data = requests.get(self.urlEdit.text()).content
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        self.imageLabel.setPixmap(pixmap)
        self.imageLabel.setFixedSize(225, 320)

# if __name__ == '__main__':
#     app = QApplication([])
#
#     w = URLView("https://kinopoiskapiunofficial.tech/images/posters/kp_small/595937.jpg")
#     # http://books.google.com/books/content?id=DdnIBgAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api
#     # https://kinopoiskapiunofficial.tech/images/posters/kp/5297246.jpg
#     # https://s4.anilist.co/file/anilistcdn/media/manga/cover/medium/23320.jpg
#     w.show()
#
#     app.exec()
