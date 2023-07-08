import sqlite3

from AnilistPython import Anilist
from PIL import Image
from PyQt6 import QtCore
from PyQt6 import QtGui
from PyQt6 import uic
from PyQt6.QtWidgets import QGridLayout, QScrollArea, QPlainTextEdit
from PyQt6.QtWidgets import QInputDialog, QFileDialog, QMessageBox
from PyQt6.QtWidgets import QWidget, QMainWindow, QPushButton, QComboBox, QToolBar, QTextEdit, QScrollBar, QHBoxLayout

from app.backend.api_kinopoisk import Kinopoisk
from app.backend.google_books import get_book
from app.frontend.a1 import UiMainWindow
from app.frontend.a2 import UiPlusWindow


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
        item = self.filter_box.model().itemFromIndex(index)
        self.load_db(item.text())
        self.set_info()
        self.swimmingButtons()
        self.tool_bar.show()
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
            "name_romaji", "ending_time", "banner_image", "airing_format",
            "airing_status", "airing_episodes", "season", "next_airing_ep",
            "is_adult", "popularity", "duration", "updated_at", "source",
        )
        try:
            anime = ani.get_anime(item)
            for key in keys_to_remove_anime:
                anime.pop(key, None)
        except IndexError:
            anime = []

        keys_to_remove_manga = (
            "name_romaji", "ending_time", "banner_image", "release_format",
            "release_status", "chapters", "volumes", "mean_score",
        )
        try:
            manga = ani.get_manga(item)
            for key in keys_to_remove_manga:
                manga.pop(key, None)
        except IndexError:
            manga = []

        keys_to_remove_books = (
            "subtitle", "authors", "publisher", "page_count",
            "print_type", "categories", "preview_link",
        )
        books = get_book(item)
        if books:
            for book in books:
                for key in keys_to_remove_books:
                    book.pop(key, None)

        results = kinop.search(item)
        # results.extend(anime)
        # results.extend(manga)
        # results.extend(books)

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

        :return: None
        """
        self.centralwidget = QWidget()
        self.gridLayout = QGridLayout(self.centralwidget)
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1062, 502))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scrollArea.setStyleSheet('background-color:  rgba(255,255,255,255);')
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.verticalScrollBar = QScrollBar(self.centralwidget)
        self.verticalScrollBar.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.gridLayout.addWidget(self.verticalScrollBar, 0, 1, 1, 1)
        self.setCentralWidget(self.centralwidget)
        self.add_button_list = {i: QPushButton(self.scrollAreaWidgetContents) for i in range(len(self.title_list))}
        i = 0
        self.verticalLayoutWidget = QWidget(self.scrollAreaWidgetContents)
        self.verticalLayout = QHBoxLayout(self.verticalLayoutWidget)
        self.horizontalLayoutWidget = QWidget(self.verticalLayoutWidget)
        for item in list_of_search_results_dict:
            self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
            title = str(item['Название'])
            rating = str(item['Оценка'])
            year = str(item['Год выпуска'])
            countries = str(item['Страны'])
            genres = str(item['Жанры'])
            text = str(
                'title:' + title + '\nrating:' + rating + '\nyear:' + year + '\ncountries:' + countries
                + '\ngenres:' + genres)
            img_button = QPushButton(self.scrollAreaWidgetContents)
            item_info = QTextEdit(self.scrollAreaWidgetContents)
            item_info.setText(text)
            self.horizontalLayout.addWidget(item_info)
            self.horizontalLayout.addSpacing(10)
            self.horizontalLayout.addWidget(img_button)
            self.verticalLayout.addWidget(self.horizontalLayoutWidget)
            add_to_plans = self.add_button_list[i]
            add_to_plans.setStyleSheet("QPushButton{\n"
                                       "    background-color: rgb(201, 164, 255);\n"
                                       "    border-radius: 10px;\n"
                                       "    padding: 5px;\n"
                                       "    width: 100px;\n"
                                       "    height: 15px;\n"
                                       "}\n"
                                       "QPushButton:hover{\n"
                                       "    background-color: rgb(157, 0, 255);\n"
                                       "}")

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
                image = Image.open(path_list_copy[1])
                image = image.resize((225, 320))
                image.save(path_list_copy[1])
                picture_button.setStyleSheet(f'background-image : url({path_list_copy[1]});')
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
        self.currect_size = [self.x(), self.y() + 30, self.width(), self.height()]
        self.size = [int(i) for i in self.currect_size]
        self.win = InputWindow()
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

    def update_db(self):
        """
        Updates the database with the new media item.

        :return: None
        """
        cur = self.connection.cursor()
        cur.execute("""INSERT INTO titles(title, status, type, progress, rating, review)
                        VALUES (?, ?, ?, ?, ?, ?)""",
                    (self.title, self.status, self.type, self.progress, self.rating, self.comment))
        cur.execute("""INSERT INTO pictures(title, path)
                        VALUES (?, ?)""", (self.title, self.redact_path))
        self.connection.commit()
        self.load_db()


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
        try:
            if self.sender().text() == '+':
                self.back_button.clicked.connect(self.main_window)
                self.button_add.clicked.connect(self.save_info)
            else:
                self.button_add.clicked.connect(self.saveReduct)
        except:
            self.button_add.clicked.connect(self.save_info)

