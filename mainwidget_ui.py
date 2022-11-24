import os
import sys
from pathlib import Path

from PyQt6 import QtCore, QtGui, QtWidgets

from PyQt6.QtCore import Qt, QCoreApplication
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QFileDialog, QToolBar, QMessageBox, QInputDialog
from PyQt6.QtCore import pyqtSlot
from auto_img_ui import Ui_ImgProcess


class Ui_MainWidget(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def setupUi(self, MainWidget):
        MainWidget.setObjectName("MainWidget")
        MainWidget.resize(800, 600)
        self.gridLayoutWidget = QtWidgets.QWidget(MainWidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(70, 80, 641, 441))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 0, 1, 1, 1)

        self.retranslateUi(MainWidget)
        QtCore.QMetaObject.connectSlotsByName(MainWidget)

    def retranslateUi(self, MainWidget):
        _translate = QtCore.QCoreApplication.translate
        MainWidget.setWindowTitle(_translate("MainWidget", "MainWidget"))
        self.pushButton.setText(_translate("MainWidget", "图像处理"))
        self.pushButton_2.setText(_translate("MainWidget", "打开摄像头"))
        self.pushButton.clicked.connect(self.get_image_path)

    def set_slot(self):
        self.pushButton.triggered.connect(self.get_image_path)

    def get_image_path(self):
        home_dir = str(Path.home())
        self.fname_list = QFileDialog.getOpenFileNames(
            self,
            'Open file',
            home_dir,
            "Image Files (*.png *.jpg *.bmp *.jpeg)"
        )
        if self.fname_list[0]:
            ui = Ui_ImgProcess(self.fname_list[0])
            ui.show()

    def get_video_path(self):
        home_dir = str(Path.home())
        fname = QFileDialog.getOpenFileName(
            self,
            'Open file',
            home_dir,
            "Video Files (*.flv *.avi *.mov *.mp4 *.wmv)"
        )
        if fname[0]:
            self.video_path = fname[0]

    # def switchcontroller(self):
    #     if self.pushButton.clicked():
    #         Ui_MainWidget.hide()
    #         Ui_ImgProcess.show() #打开新页面
    #
    #     else:
    #         QMessageBox.critical(self,'文件类型选择错误力' )
    #         return None
