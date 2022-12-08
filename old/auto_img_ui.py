from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage


# imgprocess初始化class（包括ui以及imgpath的上传）
class Ui_ImgProcess(QtWidgets.QWidget):
    def __init__(self):
        super(Ui_ImgProcess, self).__init__()
        self.setupUi(self)
        self.img_path = ['', '']
        self.image = QImage(self.img_path[0])
        self.img_pix = None

    def setupUi(self, ImgProcess):
        ImgProcess.setObjectName("ImgProcess")
        ImgProcess.resize(809, 499)
        self.exitButton = QtWidgets.QPushButton(ImgProcess)
        self.exitButton.setGeometry(QtCore.QRect(690, 0, 100, 32))
        self.exitButton.setObjectName("exitButton")
        self.img_label = QtWidgets.QLabel(ImgProcess)
        self.img_label.setGeometry(QtCore.QRect(180, 80, 421, 331))
        self.img_label.setText("")
        self.img_label.setObjectName("img_label")

        self.retranslateUi(ImgProcess)
        QtCore.QMetaObject.connectSlotsByName(ImgProcess)

    def retranslateUi(self, ImgProcess):
        _translate = QtCore.QCoreApplication.translate
        ImgProcess.setWindowTitle(_translate("ImgProcess", "Form"))
        self.exitButton.setText(_translate("ImgProcess", "退出"))

    # imgpix上传
    def update_image(self):
        self.image = QImage(self.img_path[0])
        self.img_pix = QPixmap(self.image)
        self.img_pix = self.img_pix.scaled(
            self.img_label.width(),
            self.img_label.height(),
            Qt.AspectRatioMode.KeepAspectRatio
        )
        self.img_label.setPixmap(self.img_pix)

    # def toMW(self):
    #     self.ui1 = Ui_MainWidget()
    #     self.ui1.show()
    #     self.close()
