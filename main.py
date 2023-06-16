from PIL import Image
from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton
from PyQt6.QtWidgets import QGridLayout, QScrollArea, QPlainTextEdit
from PyQt6.QtWidgets import QInputDialog, QFileDialog, QMessageBox, QStatusBar, QTabWidget
from a1 import Ui_MainWindow
from a2 import Ui_PlusWindow
from a3 import Ui_EqWindow
from PyQt6 import uic
import sqlite3
import sys


class Main(QMainWindow, Ui_MainWindow):
    """
    This is class for main window
    """

    def __init__(self):
        """
        Class Constructor.
        """
        super().__init__()
        self.eq_btn = QPushButton(self)
        self.plus_btn = QPushButton(self)
        self.set_window()
        self.set_swimming_buttons()

    def set_window(self):  # инициализация
        """
        Method sets the window parameters such as window size, background color, and widgets.
        :return: None
        """
        super().__init__()
        self.setupUi(self)
        f = open('size1.txt')
        a = [int(i) for i in f.read().split(' ')]
        f.close()
        self.setGeometry(*a)
        self.setWindowIcon(QtGui.QIcon('imgs/krug'))
        self.setStyleSheet('background-color: rgb(241, 231, 255);')
        self.connect_to_db()
        self.display_widgets_buttons()

    def set_swimming_buttons(self):  # метод для кнопок для перехода в два побочных окна
        self.plus_btn.clicked.connect(self.open_window_to_add_media_content)
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
        self.eq_btn.clicked.connect(self.open_window_with_tabs)
        self.eq_btn.setStyleSheet("QPushButton{\n"
                                  "    background-color: rgb(201, 164, 255);\n"
                                  "    border-radius: 13px;\n"
                                  "    margin: 7px;\n"
                                  "}\n"
                                  "QPushButton:hover{\n"
                                  "    background-color: rgb(162, 0, 255);\n"
                                  "}")
        self.eq_btn.setText('=')
        self.eq_btn.setFixedSize(40, 40)
        self.container()

    def container(self):  # метод для котейнера этих кнопок в статусбаре
        self.sb = QStatusBar(self)
        self.sb.setStyleSheet('background-color: rgba(0, 0, 0,0);')
        self.sb.move(10, 10)
        self.sb.addWidget(self.plus_btn)
        self.sb.addWidget(self.eq_btn)
        self.sb.setFixedSize(100, 40)

    def display_widgets_buttons(self):  # метод для отображения картинок, кнопок и информации
        scr = QScrollArea(self)
        scr.setWidgetResizable(True)
        pnl = QWidget(self)
        layout = QGridLayout(self)
        self.btns = {i: QPushButton(self) for i in range(len(self.res))}
        self.redact_btns = {i: QPushButton(self) for i in range(len(self.res))}
        self.remove_btns = {i: QPushButton(self) for i in range(len(self.res))}
        self.titles = []

        self.res.reverse()
        self.puti.reverse()
        for i in range(len(self.res)):
            pic_btn = self.btns[i]
            redact_btn = self.redact_btns[i]
            remove_btn = self.remove_btns[i]
            redact_btn.setStyleSheet("QPushButton{\n"
                                     "    background-color: rgb(201, 164, 255);\n"
                                     "    border-radius: 10px;\n"
                                     "    padding: 5px;\n"
                                     "    width: 90px;\n"
                                     "    height: 15px;\n"
                                     "}\n"
                                     "QPushButton:hover{\n"
                                     "    background-color: rgb(157, 0, 255);\n"
                                     "}")
            remove_btn.setStyleSheet("QPushButton{\n"
                                     "    background-color: rgb(201, 164, 255);\n"
                                     "    border-radius: 10px;\n"
                                     "    padding: 5px;\n"
                                     "    width: 90px;\n"
                                     "    height: 15px;\n"
                                     "}\n"
                                     "QPushButton:hover{\n"
                                     "    background-color: rgb(157, 0, 255);\n"
                                     "}")
            pic_btn.setFixedSize(225, 320)
            redact_btn.setText('edit')
            remove_btn.setText('delete')
            a = list([str(j) for j in self.res[i]])
            putin = list([str(j) for j in self.puti[i]])
            if putin[1] != '':
                im = Image.open(putin[1])
                im2 = im.resize((225, 320))
                im2.save(putin[1])
                pic_btn.setStyleSheet(f'background-image : url({putin[1]});')
            else:
                pic_btn.setStyleSheet(f'background-image : url(imgs/umol.jpg);')
            pic_btn.clicked.connect(self.select_picture)
            redact_btn.clicked.connect(self.edit_list)
            remove_btn.clicked.connect(self.remove_from_list)
            self.text = QPlainTextEdit(self)
            self.titles.append(a[0])
            pola = ['title', 'status', 'type', 'progress', 'rating', 'review']
            for k in range(6):
                self.text.appendPlainText(f'{pola[k]}: {a[k]}')
            self.text.setReadOnly(True)
            self.text.setStyleSheet('background-color: rgb(241, 231, 255);')
            layout.addWidget(pic_btn, i, 3)
            layout.addWidget(self.text, i, 2)
            grid = QGridLayout()
            wid = QWidget()
            wid.setLayout(grid)
            grid.setVerticalSpacing(1)
            grid.addWidget(redact_btn)
            grid.addWidget(remove_btn)
            layout.addWidget(wid, i, 1)
        pnl.setLayout(layout)
        scr.setWidget(pnl)
        self.setCentralWidget(scr)

    def remove_from_list(self):  # метод для удаления из списка
        for k in self.remove_btns.keys():
            if self.remove_btns[k] == self.sender():
                nam = self.titles[k]
        cur = self.connection.cursor()
        cur.execute("""DELETE from titles where название = ?""", (nam,))
        cur.execute("""DELETE from pictures where название = ?""", (nam,))
        self.connection.commit()
        self.connect_to_db()
        self.open_main_window()

    def edit_list(self):  # метод для редактирования в списке
        uic.loadUi('a2.ui', self)
        for k in self.redact_btns.keys():
            if self.redact_btns[k] == self.sender():
                self.reductObj = self.titles[k]
                self.back.hide()
                self.save_editing()

    def save_editing(self):  # метод для сохранения отредактированного
        self.vvodtext.setText(self.reductObj)
        btnsarr = [self.r1, self.r2, self.r3, self.r4, self.r5, self.r6, self.r7, self.r8, self.r9]
        for el in self.res:
            if el[0] == self.reductObj:
                self.ocenka.setMaximum(10)
                self.ocenka.setValue(el[4])
                self.statusbox.setCurrentText(el[1])
                self.otzyv.setPlainText(el[5])
                for but in btnsarr:
                    if but.text() == el[2]:
                        but.setChecked(True)
        for el in self.puti:
            if el[0] == self.reductObj:
                self.putreduct = el[1]
        cur = self.connection.cursor()
        cur.execute("""DELETE from titles where название = ?""", (self.reductObj,))
        cur.execute("""DELETE from pictures where название = ?""", (self.reductObj,))
        self.connection.commit()
        self.connect_to_db()
        self.btnadd.clicked.connect(self.save_info)

    def select_picture(self):  # метод для выбора картинки при нажатии на имгбаттон
        for k in self.btns.keys():
            if self.btns[k] == self.sender():
                fname = QFileDialog.getOpenFileName(
                    self, 'Select a picture', '',
                    'Picture (*.jpg);;Picture (*.jpg);;All files (*)')[0]
                cur = self.connection.cursor()
                cur.execute("""UPDATE pictures
                                SET путь = ?
                                WHERE title = ?""", (fname, self.titles[k]))
                self.connection.commit()
                self.btns[k].setStyleSheet(f'background-image : url({fname});')
                self.connect_to_db()
                self.open_main_window()

    def connect_to_db(self):  # метод для подключения к бд
        self.connection = sqlite3.connect('titles.db')
        self.res = self.connection.cursor().execute("""SELECT * FROM titles""").fetchall()
        self.puti = self.connection.cursor().execute("""SELECT * FROM pictures""").fetchall()

    def closeEvent(self, event):  # спрашивает точно выйти
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

    def open_window_to_add_media_content(self):  # открытие окна ввода информации
        self.a = [self.x(), self.y() + 30, self.width(), self.height()]
        f = open('size1.txt', 'w')
        a = ' '.join([str(i) for i in self.a])
        f.write(a)
        f.close()
        self.w = Window2()
        self.w.show()
        self.hide()

    def open_window_with_tabs(self):  # открытие окна списка с разделами
        self.a = [self.x(), self.y() + 30, self.width(), self.height()]
        f = open('size1.txt', 'w')
        a = ' '.join([str(i) for i in self.a])
        f.write(a)
        f.close()
        self.w = Window3()
        self.w.show()
        self.hide()

    def open_main_window(self):  # открытие главного окна
        self.w = Main()
        self.w.show()
        self.hide()

    def save_info(self):  # сохранение введенной информации в переменных
        self.name = self.vvodtext.text()
        self.status = self.statusbox.currentText()
        checked = False
        btns_arr = [self.r1, self.r2, self.r3, self.r4, self.r5, self.r6, self.r7, self.r8, self.r9]
        for but in btns_arr:
            if but.isChecked():
                self.type = but.text()
                checked = True
        if self.name == '' or not checked:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('imgs/krug'))
            msg.setText("you have not entered the data")
            msg.setWindowTitle("error")
            msg.setDetailedText("please, enter a title and type")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            msg.exec_()
            return
        if self.type in ['аnime', 'series', 'movie', 'cartoon film']:
            self.message = 'number of episodes viewed:'
        elif self.type in ['manga', 'comic book', 'manhwa', 'manhua']:
            self.message = 'number of chapters read:'
        elif self.type == 'book':
            self.message = 'number of pages read:'
        self.progress, ok_pressed = QInputDialog.getText(self, "progress",
                                                         self.message)
        self.ocenk = self.ocenka.text()
        self.otzv = self.otzyv.toPlainText()
        if ok_pressed:
            self.update_db()
        self.open_main_window()

    def update_db(self):  # изменение информации в бд
        cur = self.connection.cursor()
        cur.execute("""INSERT INTO titles(название, статус, тип, прогресс, оценка, отзыв) VALUES(?,?,?,?,?,?)""",
                    (self.name, self.status, self.type, self.progress, self.ocenk, self.otzv))
        try:
            cur.execute("""INSERT INTO pictures(title,путь) VALUES(?,?)""", (self.name, self.putreduct))
        except:
            cur.execute("""INSERT INTO pictures(title,путь) VALUES(?,?)""", (self.name, ''))
        self.connection.commit()


class Window2(Main, Ui_PlusWindow, Ui_MainWindow):  # класс окна ввода
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ocenka.setMaximum(10)
        try:
            if self.sender().text() == '+':
                self.back.clicked.connect(self.open_main_window)
                self.btnadd.clicked.connect(self.save_info)

            else:
                self.btnadd.clicked.connect(self.save_editing)
        except:
            self.btnadd.clicked.connect(self.save_info)


class Window3(Main, Ui_EqWindow):  # класс окна списка с разделами
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.spiski()

    def spiski(self):  # метод для заполнения окна списков
        grid = QGridLayout(self)
        tab = QTabWidget(self)
        tab.adjustSize()
        statuslist = ['already watched', 'currently watching', 'add in watchlist',
                      'already read', 'currently reading', 'add in readlist']
        maxwidth = 0
        for i in range(6):
            content = QScrollArea(self)
            content.setWidgetResizable(True)
            w = QWidget()
            lay = QGridLayout(self)
            lay.setAlignment(Qt.AlignmentFlag.AlignLeft)
            for el in self.res:
                a = list([str(j) for j in el])
                if el[1] == statuslist[i]:
                    txt = '\n'.join(i.upper() for i in
                                    [f'title: {a[0]}', f'status: {a[1]}', f'type: {a[2]}', f'progress: {a[3]}',
                                     f'rating: {a[4]}', f'review: {a[5]}'])
                    title = QPlainTextEdit(txt, self)
                    title.setStyleSheet('background-color: rgba(241, 231, 255, 50);')
                    title.setFixedWidth(self.width())
                    title.adjustSize()
                    title.setReadOnly(True)
                    if title.width() > maxwidth:
                        maxwidth = title.width()
                    lay.addWidget(title)
            w.setLayout(lay)
            content.setWidget(w)
            tab.addTab(content, statuslist[i])
            grid.addWidget(tab)
            self.setCentralWidget(tab)
            self.setMinimumWidth(maxwidth + 30)
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec())
