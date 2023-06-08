from PIL import Image
from PyQt6 import QtGui
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton
from PyQt6.QtWidgets import QGridLayout, QScrollArea, QPlainTextEdit
from PyQt6.QtWidgets import QInputDialog, QFileDialog, QMessageBox, QStatusBar, QTabWidget
from PyQt6.QtWidgets import QApplication
from a1 import Ui_MainWindow
from a2 import Ui_PlusWindow
from a3 import Ui_EqWindow
from PyQt6 import uic
import sqlite3
import sys


class Main(QMainWindow, Ui_MainWindow):  # класс главного окна
    def __init__(self):
        super().__init__()
        self.initialize()

        # QApplication.installEventFilter(self)
        def mousePressEvent(self, event):
            if event.key() == Qt.Key_Plus:
                self.newWindow()
                return True
            elif event.key() == Qt.Key_Escape:
                self.close()
            elif event.key() == Qt.Key_Equal:
                self.listWindow()
                return True
            elif event.key() == (Qt.Key_Control and Qt.Key_Z):
                self.oldWindow()
                return True

        self.swimmingButtons()

    def initialize(self):  # инициализация
        super().__init__()
        self.setupUi(self)
        f = open('size1.txt')
        a = [int(i) for i in f.read().split(' ')]
        f.close()
        self.setGeometry(*a)
        self.setWindowIcon(QtGui.QIcon('imgs/krug'))
        self.setStyleSheet('background-color: rgb(241, 231, 255);')
        self.loadsubd()
        self.kartinkiknopochki()

    def swimmingButtons(self):  # метод для кнопок для перехода в два побочных окна
        self.plusbtn = QPushButton(self)
        self.plusbtn.clicked.connect(self.newWindow)
        self.plusbtn.setStyleSheet("QPushButton{\n"
                                   "    background-color: rgb(201, 164, 255);\n"
                                   "    border-radius: 13px;\n"
                                   "    margin: 7px;\n"
                                   "}\n"
                                   "QPushButton:hover{\n"
                                   "    background-color: rgb(162, 0, 255);\n"
                                   "}")
        self.plusbtn.setText('+')
        self.plusbtn.setFixedSize(40, 40)
        self.eqbtn = QPushButton(self)
        self.eqbtn.clicked.connect(self.listWindow)
        self.eqbtn.setStyleSheet("QPushButton{\n"
                                 "    background-color: rgb(201, 164, 255);\n"
                                 "    border-radius: 13px;\n"
                                 "    margin: 7px;\n"
                                 "}\n"
                                 "QPushButton:hover{\n"
                                 "    background-color: rgb(162, 0, 255);\n"
                                 "}")
        self.eqbtn.setText('=')
        self.eqbtn.setFixedSize(40, 40)
        self.conteiner()

    def conteiner(self):  # метод для котейнера этих кнопок в статусбаре
        self.sb = QStatusBar(self)
        self.sb.setStyleSheet('background-color: rgba(0, 0, 0,0);')
        self.sb.move(10, 10)
        self.sb.addWidget(self.plusbtn)
        self.sb.addWidget(self.eqbtn)
        self.sb.setFixedSize(100, 40)

    def kartinkiknopochki(self):  # метод для отображения картинок, кнопок и информации
        scr = QScrollArea(self)
        scr.setWidgetResizable(True)
        pnl = QWidget(self)
        layout = QGridLayout(self)
        self.btns = {i: QPushButton(self) for i in range(len(self.res))}
        self.reductbtns = {i: QPushButton(self) for i in range(len(self.res))}
        self.removebtns = {i: QPushButton(self) for i in range(len(self.res))}
        self.nazv = []

        self.res.reverse()
        self.puti.reverse()
        for i in range(len(self.res)):
            picbt = self.btns[i]
            reductbt = self.reductbtns[i]
            removebt = self.removebtns[i]
            reductbt.setStyleSheet("QPushButton{\n"
                                   "    background-color: rgb(201, 164, 255);\n"
                                   "    border-radius: 10px;\n"
                                   "    padding: 5px;\n"
                                   "    width: 90px;\n"
                                   "    height: 15px;\n"
                                   "}\n"
                                   "QPushButton:hover{\n"
                                   "    background-color: rgb(157, 0, 255);\n"
                                   "}")
            removebt.setStyleSheet("QPushButton{\n"
                                   "    background-color: rgb(201, 164, 255);\n"
                                   "    border-radius: 10px;\n"
                                   "    padding: 5px;\n"
                                   "    width: 90px;\n"
                                   "    height: 15px;\n"
                                   "}\n"
                                   "QPushButton:hover{\n"
                                   "    background-color: rgb(157, 0, 255);\n"
                                   "}")
            picbt.setFixedSize(225, 320)
            reductbt.setText('редактировать')
            removebt.setText('удалить')
            a = list([str(j) for j in self.res[i]])
            putin = list([str(j) for j in self.puti[i]])
            if putin[1] != '':
                im = Image.open(putin[1])
                im2 = im.resize((225, 320))
                im2.save(putin[1])
                picbt.setStyleSheet(f'background-image : url({putin[1]});')
            else:
                picbt.setStyleSheet(f'background-image : url(imgs/umol.jpg);')
            picbt.clicked.connect(self.vybratkartinku)
            reductbt.clicked.connect(self.reductirovat)
            removebt.clicked.connect(self.udalit)
            self.text = QPlainTextEdit(self)
            self.nazv.append(a[0])
            pola = ['название', 'статус', 'тип', 'прогресс', 'оценка', 'отзыв']
            for k in range(6):
                self.text.appendPlainText(f'{pola[k]}: {a[k]}')
            self.text.setReadOnly(True)
            self.text.setStyleSheet('background-color: rgb(241, 231, 255);')
            layout.addWidget(picbt, i, 3)
            layout.addWidget(self.text, i, 2)
            grid = QGridLayout()
            wid = QWidget()
            wid.setLayout(grid)
            grid.setVerticalSpacing(1)
            grid.addWidget(reductbt)
            grid.addWidget(removebt)
            layout.addWidget(wid, i, 1)
        pnl.setLayout(layout)
        scr.setWidget(pnl)
        self.setCentralWidget(scr)

    def udalit(self):  # метод для удаления из списка
        for k in self.removebtns.keys():
            if self.removebtns[k] == self.sender():
                nam = self.nazv[k]
        cur = self.connection.cursor()
        cur.execute("""DELETE from titles where название = ?""", (nam,))
        cur.execute("""DELETE from pictures where название = ?""", (nam,))
        self.connection.commit()
        self.loadsubd()
        self.oldWindow()

    def reductirovat(self):  # метод для редактирования в списке
        uic.loadUi('a2.ui', self)
        for k in self.reductbtns.keys():
            if self.reductbtns[k] == self.sender():
                self.reductObj = self.nazv[k]
                self.back.hide()
                self.saveReduct()

    def saveReduct(self):  # метод для сохранения отредактированного
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
        self.loadsubd()
        self.btnadd.clicked.connect(self.save)

    def vybratkartinku(self):  # метод для выбора картинки при нажатии на имгбаттон
        for k in self.btns.keys():
            if self.btns[k] == self.sender():
                fname = QFileDialog.getOpenFileName(
                    self, 'Выбрать картинку', '',
                    'Картинка (*.jpg);;Картинка (*.jpg);;Все файлы (*)')[0]
                cur = self.connection.cursor()
                cur.execute("""UPDATE pictures
                                SET путь = ?
                                WHERE название= ?""", (fname, self.nazv[k]))
                self.connection.commit()
                self.btns[k].setStyleSheet(f'background-image : url({fname});')
                self.loadsubd()
                self.oldWindow()

    def loadsubd(self):  # метод для подключения к бд
        self.connection = sqlite3.connect('titles.db')
        self.res = self.connection.cursor().execute("""SELECT * FROM titles""").fetchall()
        self.puti = self.connection.cursor().execute("""SELECT * FROM pictures""").fetchall()

    def closeEvent(self, event):  # спрашивает точно выйти
        close = QMessageBox()
        close.setText('уверены что хотите выйти?')
        close.setWindowTitle(' ')
        close.setWindowIcon(QtGui.QIcon('imgs/krug'))
        close.setStandardButtons(QMessageBox.StandardButton.Close | QMessageBox.StandardButton.Yes)
        close = close.exec()
        if close == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()

    def newWindow(self):  # открытие окна ввода информации
        self.a = [self.x(), self.y() + 30, self.width(), self.height()]
        f = open('size1.txt', 'w')
        a = ' '.join([str(i) for i in self.a])
        f.write(a)
        f.close()
        self.w = Window2()
        self.w.show()
        self.hide()

    def listWindow(self):  # открытие окна списка с разделами
        self.a = [self.x(), self.y() + 30, self.width(), self.height()]
        f = open('size1.txt', 'w')
        a = ' '.join([str(i) for i in self.a])
        f.write(a)
        f.close()
        self.w = Window3()
        self.w.show()
        self.hide()

    def oldWindow(self):  # открытие главного окна
        self.w = Main()
        self.w.show()
        self.hide()

    def save(self):  # сохранение введенной информации в переменных
        self.name = self.vvodtext.text()
        self.status = self.statusbox.currentText()
        vybr = False
        btnsarr = [self.r1, self.r2, self.r3, self.r4, self.r5, self.r6, self.r7, self.r8, self.r9]
        for but in btnsarr:
            if but.isChecked():
                self.type = but.text()
                vybr = True
        if self.name == '' or not vybr:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('imgs/krug'))
            msg.setText("вы не ввели данные")
            msg.setWindowTitle("ошибка")
            msg.setDetailedText("нужно обязательно ввести название и тип")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.exec_()
            return
        if self.type in ['аниме', 'сериал', 'фильм', 'мультфильм']:
            self.message = 'серий просмотрено:'
        elif self.type in ['манга', 'комикс', 'манхва', 'маньхуа']:
            self.message = 'глав прочитано:'
        elif self.type == 'книга':
            self.message = 'страниц прочитано:'
        self.progress, ok_pressed = QInputDialog.getText(self, "прогресс",
                                                         self.message)
        self.ocenk = self.ocenka.text()
        self.otzv = self.otzyv.toPlainText()
        if ok_pressed:
            self.updatesubd()
        self.oldWindow()

    def updatesubd(self):  # изменение информации в бд
        cur = self.connection.cursor()
        cur.execute("""INSERT INTO titles(название, статус, тип, прогресс, оценка, отзыв) VALUES(?,?,?,?,?,?)""",
                    (self.name, self.status, self.type, self.progress, self.ocenk, self.otzv))
        try:
            cur.execute("""INSERT INTO pictures(название,путь) VALUES(?,?)""", (self.name, self.putreduct))
        except:
            cur.execute("""INSERT INTO pictures(название,путь) VALUES(?,?)""", (self.name, ''))
        self.connection.commit()


class Window2(Main, Ui_PlusWindow, Ui_MainWindow):  # класс окна ввода
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ocenka.setMaximum(10)
        try:
            if self.sender().text() == '+':
                self.back.clicked.connect(self.oldWindow)
                self.btnadd.clicked.connect(self.save)

            else:
                self.btnadd.clicked.connect(self.saveReduct)
        except:
            self.btnadd.clicked.connect(self.save)


class Window3(Main, Ui_EqWindow):  # класс окна списка с разделами
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.spiski()

    def spiski(self):  # метод для заполнения окна списков
        grid = QGridLayout(self)
        tab = QTabWidget(self)
        tab.adjustSize()
        statuslist = ['просмотрено', 'смотрю', 'буду смотреть', 'прочитано', 'читаю', 'буду читать']
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
                                    [f'название: {a[0]}', f'статус: {a[1]}', f'тип: {a[2]}', f'прогресс: {a[3]}',
                                     f'оценка: {a[4]}', f'отзыв: {a[5]}'])
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
        backbtn.clicked.connect(self.oldWindow)
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
