from PyQt5 import Qt
from urllib import request


class URLView(Qt.QWidget):
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
        layout = Qt.QVBoxLayout(self)

        self.urlEdit = Qt.QLineEdit()
        self.urlEdit.setText(url)

        self.imageLabel = Qt.QLabel()
        self.imageLabel.setScaledContents(True)
        layout.addWidget(self.imageLabel)

        self._load_image_from_url()

    def _load_image_from_url(self):
        """
        Loads the image data from the specified URL and sets it in the imageLabel widget.
        """

        data = request.urlopen(self.urlEdit.text()).read()
        pixmap = Qt.QPixmap()
        pixmap.loadFromData(data)
        self.imageLabel.setPixmap(pixmap)


if __name__ == '__main__':
    app = Qt.QApplication([])

    w = URLView("https://moodle.innopolis.university/pluginfile.php/1/theme_academi/logo/1686640507/logo.png")

    w.show()

    app.exec()
