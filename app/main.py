from PIL import Image
from PyQt6 import QtGui
from PyQt6.QtWidgets import QWidget, QMainWindow, QPushButton
from PyQt6.QtWidgets import QGridLayout, QScrollArea, QPlainTextEdit
from PyQt6.QtWidgets import QInputDialog, QFileDialog, QMessageBox, QStatusBar
from PyQt6.QtWidgets import QApplication
from app.frontend.a1 import UiMainWindow
from app.frontend.a2 import UiPlusWindow
from PyQt6 import uic
import sqlite3
import sys


class Main(QMainWindow, UiMainWindow):
    """
        Main window
        """

    def __init__(self):
        super().__init__()
        self.size = [433, 124, 693, 614]
        self.eq_btn = QPushButton(self)
        self.plus_btn = QPushButton(self)
        self.initialize()
        self.swimmingButtons()

    def initialize(self):
        """
        Method for initialization
        :return:
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
        Method for swimming add_media and filter_media buttons
        :return:
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

        self.eq_btn.setStyleSheet("QPushButton{\n"
                                  "    background-color: rgb(201, 164, 255);\n"
                                  "    border-radius: 13px;\n"
                                  "    margin: 7px;\n"
                                  "}\n"
                                  "QPushButton:hover{\n"
                                  "    background-color: rgb(162, 0, 255);\n"
                                  "}")
        self.eq_btn.setText('=')
        self.eq_btn.setFixedSize(60, 40)
        self.container()

    def container(self):
        self.status_bar = QStatusBar(self)
        self.status_bar.setStyleSheet('background-color:  rgba(0,0,0,0);')
        self.status_bar.move(10, 10)
        self.status_bar.addWidget(self.plus_btn)
        self.status_bar.addWidget(self.eq_btn)
        self.status_bar.setFixedSize(100, 40)

    def set_info(self):
        """
        Method for setting list of media
        :return:
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
        Method for removing from media list
        :return:
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
        Method for redacting media list items
        :return:
        """
        uic.loadUi('frontend/a2.ui', self)
        for k in self.redact_button_list.keys():
            if self.redact_button_list[k] == self.sender():
                self.reductObj = self.name_list[k]
                self.back_button.hide()
                self.save_redacted_item()

    def save_redacted_item(self):
        """
        Method for saving redacted media list item
        :return:
        """
        self.title_input.setText(self.reductObj)
        media_type_array = [self.r1, self.r2, self.r3, self.r4, self.r5, self.r6, self.r7, self.r8, self.r9]
        print(*self.title_list)
        print(self.reductObj)
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
        Method for choosing image of media list item
        :return:
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

    def load_db(self):
        """
        Method for connecting to database
        :return:
        """
        self.connection = sqlite3.connect('../titles.db')
        self.title_list = self.connection.cursor().execute("""SELECT * FROM titles""").fetchall()
        self.path_list = self.connection.cursor().execute("""SELECT * FROM pictures""").fetchall()

    def input_window(self):
        """
        Method for opening input_window
        :return:
        """
        self.currect_size = [self.x(), self.y() + 30, self.width(), self.height()]
        self.size = [int(i) for i in self.currect_size]
        self.win = InputWindow()
        self.win.show()
        self.hide()

    def main_window(self):
        """
        Method foe opening main_window
        :return:
        """
        self.win = Main()
        self.win.show()
        self.hide()

    def save_info(self):
        """
        Method for saving information from user's input
        :return:
        """
        self.title = self.title_input.text()
        self.status = self.status_combo_box.currentText()
        choice = False
        checkboxes = [self.r1, self.r2, self.r3, self.r4, self.r5, self.r6, self.r7, self.r8, self.r9]
        print(1)
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
        Updates database
        :return:
        """
        cur = self.connection.cursor()
        cur.execute("""INSERT INTO titles(title, status, type, progress, rating, comment) VALUES(?,?,?,?,?,?)""",
                    (self.title, self.status, self.type, self.progress, self.rating, self.comment))
        try:
            cur.execute("""INSERT INTO pictures(title, path) VALUES(?,?)""", (self.title, self.putreduct))
        except:
            cur.execute("""INSERT INTO pictures(title,path) VALUES(?,?)""", (self.title, ''))
        self.connection.commit()


class InputWindow(Main, UiPlusWindow, UiMainWindow):
    """
    Input window class
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.rating_spin_box.setMaximum(10)
        try:
            if self.sender().text() == '+':
                self.back_button.clicked.connect(self.main_window)
                self.button_add.clicked.connect(self.save_info)

            else:
                self.button_add.clicked.connect(self.saveReduct)
        except:
            self.button_add.clicked.connect(self.save_info)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec())
