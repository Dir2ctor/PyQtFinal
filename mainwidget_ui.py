from pathlib import Path

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QFileDialog, QMenuBar, QWidgetAction

class Ui_MainWidget(QtWidgets.QWidget):
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

    def set_slot(self):
        # self.pushButton.clicked.connect(self.get_image_path)
        ...

    def get_image_path(self):
        home_dir = str(Path.home())
        fname_list = QFileDialog.getOpenFileNames(
            self,
            'Open file',
            home_dir,
            "Image Files (*.png *.jpg *.bmp *.jpeg)"
        )
        print(fname_list)
        if fname_list[0]:
            return fname_list[0]
        else:
            return None

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