import sqlite3

import requests
from AnilistPython import Anilist
from PIL import Image
from PyQt6 import QtCore
from PyQt6 import QtGui
from PyQt6 import uic
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QGridLayout, QScrollArea, QPlainTextEdit, QVBoxLayout, QSizePolicy, QLabel
from PyQt6.QtWidgets import QInputDialog, QFileDialog, QMessageBox
from PyQt6.QtWidgets import QWidget, QMainWindow, QPushButton, QComboBox, QToolBar, QTextEdit, QScrollBar, QHBoxLayout
from PyQt6.uic.properties import QtWidgets
from matplotlib.image import imread

from app.backend.api_kinopoisk import Kinopoisk
from app.backend.google_books import get_book
from app.frontend.a1 import UiMainWindow
from app.frontend.a2 import UiPlusWindow
from app.frontend.a3 import UiAddFromSearchWindow
from app.backend.URLhandler import URLView


class MainWindow(QMainWindow, UiMainWindow):
    """
    The Main class represents the main window of the application.

    Attributes:
        size (list): A list of integers representing the size of the main window.
        plus_btn (QPushButton): A button for adding media items.
        filter_box (QComboBox): A combo box for filtering media items by category.
        search_media (QTextEdit): A text edit for entering search keywords.
        search_btn (QPushButton): A button for initiating a search.
        connection (sqlite3.Connection): A connection object for connecting to the database.

    Methods:
        initialize(): Initializes the main window.
        swimmingButtons(): Sets up the buttons and UI elements for adding and filtering media items.
        filter_by_category(index): Filters media items by the selected category.
        search_item(): Initiates a search for media items based on the entered keyword.
        container(): Sets up the toolbar and UI elements for the main window.
        set_search_info(list_of_search_results_dict): Sets the search results in the UI.
        set_info(): Sets up the UI with the list of media items.
        remove_from_list(): Removes a media item from the list.
        redact_list_item(): Allows editing a media item in the list.
        save_redacted_item(): Saves the changes made to a media item.
        choose_picture(): Allows selecting an image for a media item.
        load_db(category='all'): Loads media items from the database.
        input_window(): Opens the input window for adding a new media item.
        main_window(): Opens the main window.
        save_info(): Saves the information entered in the input window.
        update_db(): Updates the database with the new media item.

    """

    def __init__(self):
        """
        Initializes a new instance of the Main class.

        It sets the initial size of the main window, initializes UI elements, and connects signals to slots.
        """
        super().__init__()
        self.size = [433, 124, 693, 614]
        self.plus_btn = QPushButton(self)
        self.initialize()
        self.swimmingButtons()

    def initialize(self):
        """
        Initializes the main window.

        It sets up the UI, window size, window icon, and background color. It also loads the database and sets the initial information.

        :return: None
        """
        super().__init__()
        self.setupUi(self)
        self.setGeometry(*self.size)
        self.setWindowIcon(QtGui.QIcon('imgs/krug'))
        self.setStyleSheet('background-color: rgb(241, 231, 255);')
        self.load_db()
        self.set_info()

    def swimmingButtons(self):
        """
        Sets up the buttons and UI elements for adding and filtering media items.

        :return: None
        """
        self.plus_btn.clicked.connect(self.input_window)
        self.plus_btn.setStyleSheet("QPushButton{\n"
                                    "    background-color: rgb(201, 164, 255);\n"
                                    "    border-radius: 13px;\n"
                                    "    margin: 7px;\n"
                                    "}\n"
                                    "QPushButton:hover{\n"
                                    "    background-color: rgb(162, 0, 255);\n"
                                    "}")
        self.plus_btn.setText('+')
        self.plus_btn.setFixedSize(40, 40)

        self.filter_box = QComboBox(self)
        self.filter_box.setFixedSize(70, 40)
        self.filter_box.setStyleSheet("QComboBox{\n"
                                      "    background-color: rgb(230, 208, 255);\n"
                                      "    border-radius: 20px;\n"
                                      "    width: 4px;\n"
                                      "    height: 40px;\n"
                                      "}\n"
                                      "QComboBox:hover{\n"
                                      "    background-color: rgb(255, 255, 255);\n"
                                      "}")

        self.filter_box.addItem("all")
        self.filter_box.addItem("planned")
        self.filter_box.addItem("progress")
        self.filter_box.addItem("finished")

        self.filter_box.view().pressed.connect(self.filter_by_category)

        self.search_media = QTextEdit(self)
        self.search_media.setFixedSize(300, 30)
        self.search_media.setStyleSheet("QTextEdit{\n"
                                        "    background-color: rgb(230, 208, 255);\n"
                                        "    border-radius: 15px;\n"
                                        "    width: 400px;\n"
                                        "    height: 30px;\n"
                                        "}\n"
                                        "QTextEdit:hover{\n"
                                        "    background-color: rgb(255, 255, 255);\n"
                                        "}")

        self.search_btn = QPushButton(self)
        self.search_btn.clicked.connect(self.search_item)
        self.search_btn.setStyleSheet("QPushButton{\n"
                                      "    background-color: rgb(201, 164, 255);\n"
                                      "    border-radius: 15px;\n"
                                      "    margin: 7px;\n"
                                      "}\n"
                                      "QPushButton:hover{\n"
                                      "    background-color: rgb(162, 0, 255);\n"
                                      "}")
        self.search_btn.setIcon(QtGui.QIcon('imgs/search'))
        self.search_btn.setFixedSize(45, 45)

        self.container()

    def filter_by_category(self, index):
        """
        Filters media items by the selected category.

        Args:
            index (QtCore.QModelIndex): The index of the selected category in the filter combo box.

        :return: None
        """
        self.removeToolBar(self.tool_bar)
        item = self.filter_box.model().itemFromIndex(index)
        self.load_db(item.text())
        self.set_info()
        self.swimmingButtons()
        self.setStyleSheet(
            "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, "
            "stop:0 rgba(234, 203, 239, 100), stop:0.52 rgba(255, 255, 255, 255), stop:0.565 rgba(82, 121, 76, 100), "
            "stop:0.65 rgba(159, 235, 148, 100), stop:0.721925 rgba(255, 238, 150, 100), "
            "stop:0.77 rgba(255, 128, 128, 100), stop:0.89 rgba(191, 128, 255, 100), stop:1 rgba(241, 231, 255, 255));")

        self.filter_box.setCurrentText(item.text())

    def search_item(self):
        """
        Initiates a search for media items based on the entered keyword.

        :return: None
        """
        item = str(self.search_media.toPlainText())

        kinop = Kinopoisk()
        ani = Anilist()

        keys_to_remove_anime = (
            "banner_image", "airing_format", "airing_status", "season",
            "next_airing_ep", "is_adult", "popularity", "updated_at", "source",
        )
        try:
            anime = ani.get_anime(item)
            for key in keys_to_remove_anime:
                anime.pop(key, None)
        except IndexError:
            anime = {}

        keys_to_remove_manga = (
            "banner_image", "release_format", "release_status",
            "volumes", "mean_score", "synonyms"
        )
        try:
            manga = ani.get_manga(item)
            for key in keys_to_remove_manga:
                manga.pop(key, None)
        except IndexError:
            manga = {}

        keys_to_remove_books = (
            "publisher", "print_type", "categories", "preview_link",
        )
        books = get_book(item)
        if books:
            for book in books:
                for key in keys_to_remove_books:
                    book.pop(key, None)

        results = kinop.search(item)
        if anime:
            anime_fixed = {}
            for key, value in anime.items():
                if value is None or value == []:
                    continue
                if isinstance(value, list):
                    anime_fixed[key] = ", ".join(value)
                else:
                    anime_fixed[key] = value
            results.extend([anime_fixed])

        if manga:
            manga_fixed = {}
            for key, value in manga.items():
                if value is None or value == []:
                    continue
                if isinstance(value, list):
                    manga_fixed[key] = ", ".join(value)
                else:
                    manga_fixed[key] = value
            results.extend([manga_fixed])

        if books:
            books_fixed = []
            for book in books:
                book_fixed = {}
                for key, value in book.items():
                    if value is None or value == []:
                        continue
                    if isinstance(value, list):
                        book_fixed[key] = ", ".join(value)
                    else:
                        book_fixed[key] = value
                books_fixed.append(book_fixed)
            results.extend(books_fixed)

        self.set_search_info(results)

    def container(self):
        """
        Sets up the toolbar and UI elements for the main window.

        :return: None
        """
        self.tool_bar = QToolBar(self)
        self.tool_bar.setStyleSheet('background-color:  rgba(0,0,0,0);')
        self.tool_bar.move(10, 0)
        self.tool_bar.addWidget(self.plus_btn)
        self.tool_bar.addWidget(self.filter_box)
        self.tool_bar.addSeparator()
        self.tool_bar.addWidget(self.search_media)
        self.tool_bar.addWidget(self.search_btn)
        self.tool_bar.setFixedSize(self.width(), 50)
        self.addToolBar(self.tool_bar)

    def set_search_info(self, list_of_search_results_dict):
        """
        Sets the search results in the UI.

        Args:
            list_of_search_results_dict (list): A list of dictionaries containing information about the search results.
                                        Each dictionary should have the following keys:
                                        - "Название" (str): The movie's title in Russian.
                                        - "Оценка" (str): The movie's rating on Kinopoisk.
                                        - "Год выпуска" (int): The year the movie was released.
                                        - "Страны" (str): A comma-separated string of the movie's countries.
                                        - "Жанры" (str): A comma-separated string of the movie's genres.
                                        Or:
                                        - name_romaji (str): The manga's title in romaji.
                                        - name_english (str): The manga's title in English.
                                        - starting_time (str): The manga's starting time.
                                        - ending_time (str): The manga's ending time.
                                        - cover_image (str): The manga's poster image.
                                        - banner_image (str): The manga's banner image.
                                        - airing_format (str): The manga's airing format.
                                        - airing_status (str): The manga's airing status.
                                        - airing_episodes (str): The manga's airing episodes.
                                        - season (str): The manga's season.
                                        - desc (str): The manga's description.
                                        - average_score (str): The manga's average score.
                                        - genres (list): List of a genres of a manga.
                                        - next_airing_ep (str): The manga's next airing episode.
                                        Or:
                                        - name_romaji (str): THe anime's title in romaji.
                                        - name_english (str): The anime's title in English.
                                        - starting_time (str): The anime's starting time.
                                        - ending_time (str): The anime's ending time.
                                        - cover_image (str): The anime's poster image.
                                        - banner_image (str): The anime's banner image.
                                        - release_format (str): The anime's release format.
                                        - release_status (str): The anime's release status.
                                        - chapters (str): The anime's chapters.
                                        - volumes (str): The anime's volumes.
                                        - desc (str): The anime's description.
                                        - average_score (str): The anime's average score.
                                        - mean_score (str): The anime's mean score.
                                        - genres (list): List of a genres of a anime.
                                        - next_airing_ep (str): The anime's next airing episode.
                                        Or:
                                        - title (str): The book's title.
                                        - subtitle (str): The book's subtitle.
                                        - authors (list): The list of book's authors.
                                        - publisher (str): The book's publisher.
                                        - published_date (str): The book's published date.
                                        - page_count (int): The book's page count.
                                        - print_type (str): The book's print type.
                                        - categories (list): The list of book's categories.
                                        - image_link_thumbnail (str): The book's thumbnail image.
                                        - language (str): The book's language.
                                        - description (str): The book's description.
                                        - preview_link (str): The book's preview link.
                                        - canonical_link (str): The book's canonical link.

        :return: None
        """
        self.removeToolBar(self.tool_bar)
        self.centralwidget = QWidget()
        self.gridLayout = QGridLayout(self.centralwidget)
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1062, 502))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scrollArea.setStyleSheet('background-color:  rgba(255,255,255,255);')
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)

        self.scrollArea.setStyleSheet(
            "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, "
            "stop:0 rgba(234, 203, 239, 50), stop:0.52 rgba(0, 0, 0, 0), stop:0.565 rgba(82, 121, 76, 33), "
            "stop:0.65 rgba(159, 235, 148, 50), stop:0.721925 rgba(255, 238, 150, 50), "
            "stop:0.77 rgba(255, 128, 128, 50), stop:0.89 rgba(191, 128, 255, 50), stop:1 rgba(241, 231, 255, 255));")
        add_button_list = []
        title_list = []
        type_list = []

        for item in list_of_search_results_dict:
            horizontalLayoutWidget = QWidget(self.scrollAreaWidgetContents)
            horizontalLayout = QHBoxLayout(horizontalLayoutWidget)

            text = ""
            for key, value in item.items():
                if key == "Ссылка на постер фильма":
                    Params.url_list.append(value)
                elif key == "cover_image":
                    Params.url_list.append(value)
                elif key == "image_link_thumbnail":
                    Params.url_list.append(value)
                else:
                    text += str(key) + ": " + str(value) + "\n"

            add_button = QPushButton(self.scrollAreaWidgetContents)
            add_button.setText("add to list")
            add_button.setStyleSheet("QPushButton{\n"
                                     "    background-color: rgb(201, 164, 255);\n"
                                     "    border-radius: 12px;\n"
                                     "    padding: 5px;\n"
                                     "    width: 70px;\n"
                                     "    height: 15px;\n"
                                     "}\n"
                                     "QPushButton:hover{\n"
                                     "    background-color: rgb(157, 0, 255);\n"
                                     "}")

            add_button_list += [add_button]
            item_info = QTextEdit(self.scrollAreaWidgetContents)
            item_info.setText(text)
            item_info.setStyleSheet('background-color: rgb(241, 231, 255);')
            try:
                image = URLView(Params.url_list[-1])

                horizontalLayout.addWidget(image)
            except:
                pass

            horizontalLayout.addSpacing(10)
            horizontalLayout.addWidget(item_info)
            horizontalLayout.addSpacing(10)
            horizontalLayout.addWidget(add_button)
            self.verticalLayout.addWidget(horizontalLayoutWidget)
            self.verticalLayout.addStretch()
            if item.get("Название") is not None:
                title_list += [str(item["Название"])]
                type_list += ["фильм"]
            elif item.get("name_english") is not None:
                if item.get("mean_score") is not None:
                    title_list += [str(item["name_english"])]
                    type_list += ["аниме"]
                else:
                    title_list += [str(item["name_english"])]
                    type_list += ["манга"]
            elif item.get("title") is not None:
                title_list += [str(item["title"])]
                type_list += ["книга"]
            add_button.clicked.connect(self.add_media_from_search_window)
        Params.add_button_list = add_button_list
        Params.title_list = title_list
        Params.type_list = type_list
        self.setCentralWidget(self.centralwidget)
        button_back = QPushButton()
        button_back.setStyleSheet("QPushButton{\n"
                                  "    background-color: rgb(201, 164, 255);\n"
                                  "    border-radius: 13px;\n"
                                  "    margin: 7px;\n"
                                  "}\n"
                                  "QPushButton:hover{\n"
                                  "    background-color: rgb(162, 0, 255);\n"
                                  "}")
        button_back.setFixedSize(40, 40)
        button_back.clicked.connect(self.main_window)
        button_back.setText("<-")
        toolbarWithBack = QToolBar()
        toolbarWithBack.addWidget(button_back)
        self.addToolBar(toolbarWithBack)

    def set_info(self):
        """
        Sets up the UI with the list of media items.

        :return: None
        """
        scr = QScrollArea(self)
        scr.setWidgetResizable(True)
        panel = QWidget(self)
        layout = QGridLayout(self)
        self.button_list = {i: QPushButton(self) for i in range(len(self.title_list))}
        self.redact_button_list = {i: QPushButton(self) for i in range(len(self.title_list))}
        self.remove_button_list = {i: QPushButton(self) for i in range(len(self.title_list))}
        self.name_list = []

        self.title_list.reverse()
        self.path_list.reverse()
        for i in range(len(self.title_list)):
            picture_button = self.button_list[i]
            redact_button = self.redact_button_list[i]
            remove_button = self.remove_button_list[i]
            redact_button.setStyleSheet("QPushButton{\n"
                                        "    background-color: rgb(201, 164, 255);\n"
                                        "    border-radius: 10px;\n"
                                        "    padding: 5px;\n"
                                        "    width: 100px;\n"
                                        "    height: 15px;\n"
                                        "}\n"
                                        "QPushButton:hover{\n"
                                        "    background-color: rgb(157, 0, 255);\n"
                                        "}")
            remove_button.setStyleSheet("QPushButton{\n"
                                        "    background-color: rgb(201, 164, 255);\n"
                                        "    border-radius: 10px;\n"
                                        "    padding: 5px;\n"
                                        "    width: 100px;\n"
                                        "    height: 15px;\n"
                                        "}\n"
                                        "QPushButton:hover{\n"
                                        "    background-color: rgb(157, 0, 255);\n"
                                        "}")
            picture_button.setFixedSize(225, 320)
            redact_button.setText('redact')
            remove_button.setText('remove')
            title_list_copy = list([str(j) for j in self.title_list[i]])
            path_list_copy = list([str(j) for j in self.path_list[i]])
            if path_list_copy[1] != '':
                if "https" not in path_list_copy[1]:
                    image = QIcon()
                    pixmap = QPixmap(path_list_copy[1])
                    image.addPixmap(pixmap)
                    picture_button.setIcon(image)
                    picture_button.setIconSize(QSize(225, 320))
                else:
                    image = QIcon()
                    try:
                        data = requests.get(path_list_copy[1]).content
                        pixmap = QPixmap()
                        pixmap.loadFromData(data)
                        image.addPixmap(pixmap)
                        picture_button.setIcon(image)
                        picture_button.setIconSize(QSize(225, 320))
                    except Exception:
                        picture_button.setStyleSheet(f'background-image : url(imgs/umol.jpg);')

            else:
                picture_button.setStyleSheet(f'background-image : url(imgs/umol.jpg);')
            picture_button.clicked.connect(self.choose_picture)
            redact_button.clicked.connect(self.redact_list_item)
            remove_button.clicked.connect(self.remove_from_list)
            self.list_items_text = QPlainTextEdit(self)
            self.name_list.append(title_list_copy[0])
            list_item_fields = ['title', 'status', 'type', 'progress', 'rating', 'review']
            for k in range(6):
                self.list_items_text.appendPlainText(f'{list_item_fields[k]}: {title_list_copy[k]}')
            self.list_items_text.setReadOnly(True)
            self.list_items_text.setStyleSheet('background-color: rgb(241, 231, 255);')
            layout.addWidget(picture_button, i, 3)
            layout.addWidget(self.list_items_text, i, 2)
            grid = QGridLayout()
            wid = QWidget()
            wid.setLayout(grid)
            grid.setVerticalSpacing(1)
            grid.addWidget(redact_button)
            grid.addWidget(remove_button)
            layout.addWidget(wid, i, 1)
        panel.setLayout(layout)
        scr.setWidget(panel)
        self.setCentralWidget(scr)

    def remove_from_list(self):
        """
        Removes a media item from the list.

        :return: None
        """
        remove_item_name = ""
        for k in self.remove_button_list.keys():
            if self.remove_button_list[k] == self.sender():
                remove_item_name = self.name_list[k]
        cur = self.connection.cursor()
        cur.execute("""DELETE from titles where title = ?""", (remove_item_name,))
        cur.execute("""DELETE from pictures where title = ?""", (remove_item_name,))
        self.connection.commit()
        self.load_db()
        self.main_window()

    def redact_list_item(self):
        """
        Allows editing a media item in the list.

        :return: None
        """
        self.removeToolBar(self.tool_bar)
        uic.loadUi('frontend/a2.ui', self)
        for k in self.redact_button_list.keys():
            if self.redact_button_list[k] == self.sender():
                self.reductObj = self.name_list[k]
                self.back_button.hide()
                self.save_redacted_item()

    def save_redacted_item(self):
        """
        Saves the changes made to a media item.

        :return: None
        """
        self.title_input.setText(self.reductObj)
        media_type_array = [self.r1, self.r2, self.r3, self.r4, self.r5, self.r6, self.r7, self.r8, self.r9]
        for el in self.title_list:
            if el[0] == self.reductObj:
                self.rating_spin_box.setMaximum(10)
                self.rating_spin_box.setValue(el[4])
                self.status_combo_box.setCurrentText(el[1])
                self.comment_input.setPlainText(el[5])
                for button in media_type_array:
                    if button.text() == el[2]:
                        button.setChecked(True)
        for el in self.path_list:
            if el[0] == self.reductObj:
                self.redact_path = el[1]
        cur = self.connection.cursor()
        cur.execute("""DELETE from titles where title = ?""", (self.reductObj,))
        cur.execute("""DELETE from pictures where title = ?""", (self.reductObj,))
        self.connection.commit()
        self.load_db()
        self.button_add.clicked.connect(self.save_info)

    def choose_picture(self):
        """
        Allows selecting an image for a media item.

        :return: None
        """
        for k in self.button_list.keys():
            if self.button_list[k] == self.sender():
                fname = QFileDialog.getOpenFileName(
                    self, 'Choose picture', '',
                    'Picture (*.jpg);;Picture (*.jpg);;All files (*)')[0]
                cur = self.connection.cursor()
                cur.execute("""UPDATE pictures
                                SET path = ?
                                WHERE title= ?""", (fname, self.name_list[k]))
                self.connection.commit()
                self.button_list[k].setStyleSheet(f'background-image : url({fname});')
                self.load_db()
                self.main_window()

    def load_db(self, category='all'):
        """
        Loads media items from the database.

        Args:
            category (str): The category to filter the media items by. Default is 'all' to load all items.

        :return: None
        """
        self.connection = sqlite3.connect('../titles.db')
        if category == 'all':
            self.title_list = self.connection.cursor().execute("""SELECT * FROM titles""").fetchall()
            self.path_list = self.connection.cursor().execute("""SELECT * FROM pictures""").fetchall()
            return
        self.title_list = self.connection.cursor().execute(
            """SELECT * FROM titles where status = ?""", (category,)).fetchall()
        self.path_list = self.connection.cursor().execute("""SELECT * FROM pictures where status = ?""",
                                                          (category,)).fetchall()

    def input_window(self):
        """
        Opens the input window for adding a new media item.

        :return: None
        """
        self.currect_size = [self.x(), self.y(), self.width(), self.height()]
        self.size = [int(i) for i in self.currect_size]
        self.win = InputWindow()
        self.win.show()
        self.hide()

    def add_media_from_search_window(self):
        """
        Opens the window for adding a new media item from search.

        :return: None
        """
        for k in range(len(Params.add_button_list)):
            if Params.add_button_list[k] == self.sender():
                Params.sender_index = k
        self.currect_size = [self.x(), self.y(), self.width(), self.height()]
        self.size = [int(i) for i in self.currect_size]
        self.win = AddFromSearchWindow()
        self.win.show()
        self.hide()

    def main_window(self):
        """
        Opens the main window.

        :return: None
        """
        self.win = MainWindow()
        self.win.show()
        self.hide()

    def save_info(self):
        """
        Saves the information entered in the input window.

        :return: None
        """

        self.title = self.title_input.text()
        self.status = self.status_combo_box.currentText()
        choice = False
        checkboxes = [self.r1, self.r2, self.r3, self.r4, self.r5, self.r6, self.r7, self.r8, self.r9]
        for but in checkboxes:
            if but.isChecked():
                self.type = but.text()
                choice = True
        if self.title == '' or not choice:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('imgs/krug'))
            msg.setText("You need to input title and type")
            msg.setWindowTitle("error")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            msg.exec()
            return

        self.message = 'progress'
        self.progress, ok_pressed = QInputDialog.getText(self, "progress", self.message)
        self.rating = self.rating_spin_box.text()
        self.comment = self.comment_input.toPlainText()
        if ok_pressed:
            self.update_db()
        self.main_window()

    def save_from_search_info(self):
        """
        Saves the information entered in the input window.

        :return: None
        """

        self.title = Params.title_list[Params.sender_index]
        self.type = Params.type_list[Params.sender_index]
        self.redact_path = Params.url_list[Params.sender_index]
        print(self.redact_path)

        self.status = self.status_box.currentText()
        self.message = 'progress'
        self.rating = self.rating_spin_box.text()
        self.comment = self.comment_input.toPlainText()

        self.progress, ok_pressed = QInputDialog.getText(self, "progress", self.message)
        if ok_pressed:
            self.update_db()
        self.main_window()

    def update_db(self):
        """
        Updates database
        :return:
        """
        cur = self.connection.cursor()
        cur.execute("""INSERT INTO titles(title, status, type, progress, rating, review) VALUES(?,?,?,?,?,?)""",
                    (self.title, self.status, self.type, self.progress, self.rating, self.comment))
        try:
            cur.execute("""INSERT INTO pictures(title, path, status) VALUES(?,?,?)""",
                        (self.title, self.redact_path, self.status))
        except:
            cur.execute("""INSERT INTO pictures(title, path, status) VALUES(?,)""",
                        (self.title,))
        self.connection.commit()


class InputWindow(MainWindow, UiPlusWindow, UiMainWindow):
    """
    This class represents an input window that combines the functionality of the Main, UiPlusWindow,
    and UiMainWindow classes.

    Attributes:
        Inherits attributes from Main, UiPlusWindow, and UiMainWindow classes.

    Methods:
        __init__(): Initializes the InputWindow object.
    """

    def __init__(self):
        """
        Initializes an instance of the InputWindow class.

        It sets up the user interface, including the maximum value for the rating_spin_box.
        It also connects the appropriate button click events to their corresponding functions.
        If an exception occurs while connecting the button events, it falls back to a default function.
        """
        super().__init__()  # Initialize the inherited classes
        self.setupUi(self)  # Set up the user interface
        self.rating_spin_box.setMaximum(10)  # Set the maximum value for the rating_spin_box
        self.removeToolBar(self.tool_bar)
        try:
            if self.sender().text() == '+':
                self.back_button.clicked.connect(self.main_window)
                self.button_add.clicked.connect(self.save_info)
            else:
                self.button_add.clicked.connect(self.saveReduct)
        except:
            self.button_add.clicked.connect(self.save_info)


class AddFromSearchWindow(MainWindow, UiAddFromSearchWindow, UiMainWindow):
    def __init__(self):
        super().__init__()  # Initialize the inherited classes
        self.type = None
        self.title = None
        self.setupUi(self)  # Set up the user interface
        self.rating_spin_box.setMaximum(10)  # Set the maximum value for the rating_spin_box
        self.removeToolBar(self.tool_bar)

        try:
            # self.back_button.clicked.connect(self.main_window)
            self.button_add.clicked.connect(self.save_from_search_info)
        except:
            self.button_add.clicked.connect(self.save_from_search_info)


class Params:
    title_list = []
    type_list = []
    add_button_list = []
    url_list = []
    sender_index = 0
