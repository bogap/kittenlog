# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'a1.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


def re_translate_ui(main_win):
    _translate = QtCore.QCoreApplication.translate
    main_win.setWindowTitle(_translate("MainWindow", "kitten_ฅ^•ﻌ•^ฅ_log"))


class UiMainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1102, 522)
        MainWindow.setStyleSheet(
            "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, "
            "stop:0 rgba(234, 203, 239, 100), stop:0.52 rgba(255, 255, 255, 255), stop:0.565 rgba(82, 121, 76, 100), "
            "stop:0.65 rgba(159, 235, 148, 100), stop:0.721925 rgba(255, 238, 150, 100), "
            "stop:0.77 rgba(255, 128, 128, 100), stop:0.89 rgba(191, 128, 255, 100), stop:1 rgba(241, 231, 255, 255));")
        self.central_widget = QtWidgets.QWidget(MainWindow)
        self.central_widget.setObjectName("central_widget")
        self.grid_layout = QtWidgets.QGridLayout(self.central_widget)
        self.grid_layout.setObjectName("grid_layout")
        MainWindow.setCentralWidget(self.central_widget)

        re_translate_ui(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
