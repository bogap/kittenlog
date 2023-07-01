from PyQt5 import Qt
from urllib import request


class URLView(Qt.QWidget):

    def __init__(self, url, parent=None):

        super().__init__(parent)
        # Call the constructor of the parent class (QWidget)

        layout = Qt.QVBoxLayout(self)

        self.urlEdit = Qt.QLineEdit()
        self.urlEdit.setText(url)
        # Set a URL in the QLineEdit widget

        self.imageLabel = Qt.QLabel()
        self.imageLabel.setScaledContents(True)
        layout.addWidget(self.imageLabel)
        # Set the place to image

        data = request.urlopen(self.urlEdit.text()).read()
        pixmap = Qt.QPixmap()
        pixmap.loadFromData(data)
        self.imageLabel.setPixmap(pixmap)
        # Retrieve the image data by opening the URL and load the image

if __name__ == '__main__':
    app = Qt.QApplication([])
    # Create an instance of QApplication

    w = URLView("https://moodle.innopolis.university/pluginfile.php/1/theme_academi/logo/1686640507/logo.png")
    # Create an instance of URLView

    w.show()
    # Display the URLView widget

    app.exec()
    # Start the event loop of the application
