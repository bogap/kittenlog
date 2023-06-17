import os
import sqlite3
from PIL import Image
from PyQt6 import uic, QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QMainWindow, QPushButton, QGridLayout, QScrollArea, QPlainTextEdit, QInputDialog, \
    QFileDialog, QMessageBox, QStatusBar, QTabWidget
from UI.a1 import UiMainWindow
from UI.a2 import UiInputWindow
from UI.a3 import UiTabsWindow


class MainWindow(QMainWindow, UiMainWindow):
    """
    This is class for main window......
    """

    def __init__(self):
        """
        Class Constructor sets all window parameters.
        """

        super().__init__()
        self.window_size = [7, 30, 700, 700]
        self.edit_obj = None
        self.titles = None
        self.remove_buttons = None
        self.edit_buttons = None
        self.buttons = None
        self.enter_text = None
        self.rating = None
        self.status_box = None
        self.review = None
        self.back = None
        self.add_button = None
        self.connection = None
        self.picture_titles = None
        self.paths_to_pictures = None
        self.status_bar = QStatusBar(self)
        self.equal_button = QPushButton(self)
        self.plus_button = QPushButton(self)
        self.set_window()
        self.set_swimming_buttons()

    def set_window(self):
        """
        Method sets the window parameters such a background color, and widgets displaying.

        :return: None
        """

        super().__init__()
        self.setup_ui(self)
        self.setGeometry(*self.window_size)
        self.setWindowIcon(QtGui.QIcon('imgs/krug'))
        self.setStyleSheet('background-color: rgb(241, 231, 255);')
        self.connect_to_db()
        self.display_media_list()

    def set_swimming_buttons(self):
        """
        Method for going to input window - window for adding more media content in list,
        and tabs window - window with tabs showing status of media content.

        :return: None
        """

        self.plus_button.clicked.connect(self.open_input_window)
        self.plus_button.setStyleSheet("QPushButton{\n"
                                       "    background-color: rgb(201, 164, 255);\n"
                                       "    border-radius: 13px;\n"
                                       "    margin: 7px;\n"
                                       "}\n"
                                       "QPushButton:hover{\n"
                                       "    background-color: rgb(162, 0, 255);\n"
                                       "}")
        self.plus_button.setText('+')
        self.plus_button.setFixedSize(40, 40)
        self.equal_button.clicked.connect(self.open_tabs_window)
        self.equal_button.setStyleSheet("QPushButton{\n"
                                        "    background-color: rgb(201, 164, 255);\n"
                                        "    border-radius: 13px;\n"
                                        "    margin: 7px;\n"
                                        "}\n"
                                        "QPushButton:hover{\n"
                                        "    background-color: rgb(162, 0, 255);\n"
                                        "}")
        self.equal_button.setText('=')
        self.equal_button.setFixedSize(40, 40)
        self.create_widgets()

    def create_widgets(self):
        """
        Method creates widgets for plus button - button to go to the input window,
        and equal button - button to go to the tabs window.

        :return: None
        """

        self.status_bar.setStyleSheet('background-color: rgba(0, 0, 0,0);')
        self.status_bar.move(10, 10)
        self.status_bar.addWidget(self.plus_button)
        self.status_bar.addWidget(self.equal_button)
        self.status_bar.setFixedSize(100, 40)

    def display_media_list(self):
        """
        Method displays media list in the main window.
        It sets parameters of pictures, buttons and fields with information about media content.

        :return: None
        """

        scr = QScrollArea(self)
        scr.setWidgetResizable(True)
        pnl = QWidget(self)
        layout = QGridLayout(self)
        self.buttons = {i: QPushButton(self) for i in range(len(self.picture_titles))}
        self.edit_buttons = {i: QPushButton(self) for i in range(len(self.picture_titles))}
        self.remove_buttons = {i: QPushButton(self) for i in range(len(self.picture_titles))}
        self.titles = []

        self.picture_titles.reverse()
        self.paths_to_pictures.reverse()
        for i in range(len(self.picture_titles)):
            pic_button = self.buttons[i]
            edit_button = self.edit_buttons[i]
            remove_button = self.remove_buttons[i]
            edit_button.setStyleSheet("QPushButton{\n"
                                      "    background-color: rgb(201, 164, 255);\n"
                                      "    border-radius: 10px;\n"
                                      "    padding: 5px;\n"
                                      "    width: 90px;\n"
                                      "    height: 15px;\n"
                                      "}\n"
                                      "QPushButton:hover{\n"
                                      "    background-color: rgb(157, 0, 255);\n"
                                      "}")
            remove_button.setStyleSheet("QPushButton{\n"
                                        "    background-color: rgb(201, 164, 255);\n"
                                        "    border-radius: 10px;\n"
                                        "    padding: 5px;\n"
                                        "    width: 90px;\n"
                                        "    height: 15px;\n"
                                        "}\n"
                                        "QPushButton:hover{\n"
                                        "    background-color: rgb(157, 0, 255);\n"
                                        "}")
            pic_button.setFixedSize(225, 320)
            edit_button.setText('edit')
            remove_button.setText('delete')
            a = list([str(j) for j in self.picture_titles[i]])
            putin = list([str(j) for j in self.paths_to_pictures[i]])
            if putin[1] != '':
                im = Image.open(putin[1])
                im2 = im.resize((225, 320))
                im2.save(putin[1])
                pic_button.setStyleSheet(f'background-image : url({putin[1]});')
            else:
                pic_button.setStyleSheet(f'background-image : url(imgs/umol.jpg);')
            pic_button.clicked.connect(self.select_picture)
            edit_button.clicked.connect(self.edit_list)
            remove_button.clicked.connect(self.remove_from_list)
            text = QPlainTextEdit(self)
            self.titles.append(a[0])
            fields = ['title', 'status', 'type', 'progress', 'rating', 'review']
            for k in range(6):
                text.appendPlainText(f'{fields[k]}: {a[k]}')
            text.setReadOnly(True)
            text.setStyleSheet('background-color: rgb(241, 231, 255);')
            layout.addWidget(pic_button, i, 3)
            layout.addWidget(text, i, 2)
            grid = QGridLayout()
            wid = QWidget()
            wid.setLayout(grid)
            grid.setVerticalSpacing(1)
            grid.addWidget(edit_button)
            grid.addWidget(remove_button)
            layout.addWidget(wid, i, 1)
        pnl.setLayout(layout)
        scr.setWidget(pnl)
        self.setCentralWidget(scr)

    def remove_from_list(self):
        """
        Method edits media list by removing certain media item from the list.

        :return: None
        """

        for k in self.remove_buttons.keys():
            if self.remove_buttons[k] == self.sender():
                nam = self.titles[k]
        cur = self.connection.cursor()
        cur.execute("""DELETE from titles where title = ?""", (nam,))
        cur.execute("""DELETE from pictures where title = ?""", (nam,))
        self.connection.commit()
        self.connect_to_db()
        self.open_main_window()

    def edit_list(self):
        """
        Method edits certain media item in the list.

        :return: None
        """

        path = os.path.join('../UI', 'a2.ui')
        uic.loadUi(path, self)
        # uic.loadUi('UI/a2.ui', self)
        for k in self.edit_buttons.keys():
            if self.edit_buttons[k] == self.sender():
                self.edit_obj = self.titles[k]
                self.back.hide()
                self.save_editing()

    def save_editing(self):
        """
        Method saves changes after editing certain media item in the list.

        :return: None
        """

        self.enter_text.setText(self.edit_obj)
        array_of_buttons = [self.r1, self.r2, self.r3, self.r4, self.r5, self.r6, self.r7, self.r8, self.r9]
        for item in self.picture_titles:
            if item[0] == self.edit_obj:
                self.rating.setMaximum(10)
                self.rating.setValue(item[4])
                self.status_box.setCurrentText(item[1])
                self.review.setPlainText(item[5])
                for but in array_of_buttons:
                    if but.text() == item[2]:
                        but.setChecked(True)
        for item in self.paths_to_pictures:
            if item[0] == self.edit_obj:
                self.putreduct = item[1]
        cur = self.connection.cursor()
        cur.execute("""DELETE from titles where название = ?""", (self.edit_obj,))
        cur.execute("""DELETE from pictures where название = ?""", (self.edit_obj,))
        self.connection.commit()
        self.connect_to_db()
        self.add_button.clicked.connect(self.save_info)

    def select_picture(self):
        """
        Method allows to select a picture from the files
        by clicking to image of media item in list.

        :return: None
        """

        for k in self.buttons.keys():
            if self.buttons[k] == self.sender():
                fname = QFileDialog.getOpenFileName(
                    self, 'Select a picture', '',
                    'Picture (*.jpg);;Picture (*.jpg);;All files (*)')[0]
                cur = self.connection.cursor()
                cur.execute("""UPDATE pictures
                                SET путь = ?
                                WHERE title = ?""", (fname, self.titles[k]))
                self.connection.commit()
                self.buttons[k].setStyleSheet(f'background-image : url({fname});')
                self.connect_to_db()
                self.open_main_window()

    def connect_to_db(self):
        """
        Method ensures connection to database.

        :return: None
        """

        self.connection = sqlite3.connect('titles.db')
        self.picture_titles = self.connection.cursor().execute("""SELECT * FROM titles""").fetchall()
        self.paths_to_pictures = self.connection.cursor().execute("""SELECT * FROM pictures""").fetchall()

    def closeEvent(self, event):
        """
        Method confirms that user wants to exit the main window
        by asking user.

        :param event: exit the window
        :return: None
        """

        close = QMessageBox()
        close.setText('are you sure you want to exit?')
        close.setWindowTitle(' ')
        close.setWindowIcon(QtGui.QIcon('imgs/krug'))
        close.setStandardButtons(QMessageBox.StandardButton.Close | QMessageBox.StandardButton.Yes)
        close = close.exec()
        if close == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()

    def open_input_window(self):
        """
        Method opens the input window to add new media item and enter information about it.

        :return: None
        """

        self.window_size = [self.x(), self.y() + 30, self.width(), self.height()]
        InputWindow().show()
        self.hide()

    def open_tabs_window(self):
        """
        Method opens tabs window to watch media items divided by their status in the tabs.

        :return: None
        """

        self.window_size = [self.x(), self.y() + 30, self.width(), self.height()]
        TabsWindow().show()
        self.hide()

    def open_main_window(self):
        """
        Method opens the main window

        :return: None
        """

        MainWindow().show()
        self.hide()

    def save_info(self):
        """
        Method saves information entered in input window.

        :return: None
        """

        self.name = self.enter_text.text()
        self.status = self.status_box.currentText()
        checked = False
        array_of_buttons = [self.r1, self.r2, self.r3, self.r4, self.r5, self.r6, self.r7, self.r8, self.r9]
        for button in array_of_buttons:
            if button.isChecked():
                self.type = button.text()
                checked = True
        if self.name == '' or not checked:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('imgs/krug'))
            msg.setText("you have not entered the data")
            msg.setWindowTitle("error")
            msg.setDetailedText("please, enter a title and type")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            msg.exec()
            return
        if self.type in ['аnime', 'series', 'movie', 'cartoon film']:
            self.message = 'number of episodes viewed:'
        elif self.type in ['manga', 'comic book', 'manhwa', 'manhua']:
            self.message = 'number of chapters read:'
        elif self.type == 'book':
            self.message = 'number of pages read:'
        self.progress, ok_pressed = QInputDialog.getText(self, "progress",
                                                         self.message)
        self.ocenk = self.rating.text()
        self.otzv = self.review.toPlainText()
        if ok_pressed:
            self.update_db()
        self.open_main_window()

    def update_db(self):
        """
        Method updates information in database if it was changed.

        :return: None
        """

        cur = self.connection.cursor()
        cur.execute("""INSERT INTO titles(название, статус, тип, прогресс, оценка, отзыв) VALUES(?,?,?,?,?,?)""",
                    (self.name, self.status, self.type, self.progress, self.ocenk, self.otzv))
        try:
            cur.execute("""INSERT INTO pictures(title,путь) VALUES(?,?)""", (self.name, self.putreduct))
        except Exception:
            cur.execute("""INSERT INTO pictures(title,путь) VALUES(?,?)""", (self.name, ''))
        self.connection.commit()


class InputWindow(MainWindow, UiInputWindow, UiMainWindow):
    """
    Class for input window.
    """

    def __init__(self):
        """
        Constructor sets parameters of input window and describes a window items behavior.
        """

        super().__init__()
        self.setup_ui(self)
        self.rating.setMaximum(10)
        try:
            if self.sender().text() == '+':
                self.back.clicked.connect(self.open_main_window)
                self.add_button.clicked.connect(self.save_info)

            else:
                self.add_button.clicked.connect(self.save_editing)
        except Exception:
            self.add_button.clicked.connect(self.save_info)


class TabsWindow(MainWindow, UiTabsWindow):
    """
    Class for tabs window.
    """

    def __init__(self):
        """
        Constructor sets parameters of tabs window and fills tabs.
        """

        super().__init__()
        self.setup_ui(self)
        self.fill_tabs()

    def fill_tabs(self):
        """
        Method fills tabs windows with media content corresponding to their status.

        :return: None
        """

        grid = QGridLayout(self)
        tab = QTabWidget(self)
        tab.adjustSize()
        status_list = ['already watched', 'currently watching', 'add in watchlist',
                       'already read', 'currently reading', 'add in readlist']
        max_width = 0
        number_of_tabs = 6
        for i in range(number_of_tabs):
            content = QScrollArea(self)
            content.setWidgetResizable(True)
            w = QWidget()
            lay = QGridLayout(self)
            lay.setAlignment(Qt.AlignmentFlag.AlignLeft)
            for el in self.picture_titles:
                a = list([str(j) for j in el])
                if el[1] == status_list[i]:
                    txt = '\n'.join(i.upper() for i in
                                    [f'title: {a[0]}', f'status: {a[1]}', f'type: {a[2]}', f'progress: {a[3]}',
                                     f'rating: {a[4]}', f'review: {a[5]}'])
                    title = QPlainTextEdit(txt, self)
                    title.setStyleSheet('background-color: rgba(241, 231, 255, 50);')
                    title.setFixedWidth(self.width())
                    title.adjustSize()
                    title.setReadOnly(True)
                    if title.width() > max_width:
                        max_width = title.width()
                    lay.addWidget(title)
            w.setLayout(lay)
            content.setWidget(w)
            tab.addTab(content, status_list[i])
            grid.addWidget(tab)
            self.setCentralWidget(tab)
            self.setMinimumWidth(max_width + 30)
        backbtn = QPushButton()
        backbtn.setText('<-')
        backbtn.clicked.connect(self.open_main_window)
        backbtn.setStyleSheet("QPushButton{\n"
                              "    background-color: rgb(230, 208, 255);\n"
                              "    border-radius: 15px;\n"
                              "    padding: 5px;\n"
                              "    width: 20px;\n"
                              "    height: 20px;\n"
                              "}\n"
                              "QPushButton:hover{\n"
                              "    background-color: rgb(157, 0, 255);\n"
                              "}")
        sb = QStatusBar(self)
        sb.setStyleSheet('background-color: rgba(0, 0, 0,0);')
        sb.move(self.width() - 50, 10)
        sb.addWidget(backbtn)
        sb.setFixedSize(100, 40)
