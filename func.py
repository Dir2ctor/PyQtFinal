import os
from pathlib import Path

import cv2
import numpy as np
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import Qt, QCoreApplication
from PyQt6.QtGui import QPixmap, QImage, QIcon, QTransform
from PyQt6.QtWidgets import QListWidgetItem, \
    QFileDialog, QMessageBox, QWidget, QInputDialog, QApplication

from auto_img_ui import Ui_ImgProcess
from auto_video_ui import Ui_VideoProcess


class Func(QtWidgets.QWidget, Ui_ImgProcess):

    def __init__(self):
        super().__init__()
        self.img_path = ['', '']
        self.image = QImage(self.img_path[0])
        self.img_pix = None
        self.currentImgIdx = 0
        self.currentImg = None
        self.setupUi(self)
        self.set_slider()
        self.update_image()
        self.set_slot()
        self.is_cn = True

    def set_slot(self):
        # 信号连接
        self.imgList.itemSelectionChanged.connect(self.loadImage)
        self.gray_button.clicked.connect(self.image_gray)
        self.filter_slider.sliderReleased.connect(self.image_filter)
        self.binarization_slider.sliderReleased.connect(self.image_binarization)
        self.gammar_slider.sliderReleased.connect(self.image_gammar)
        self.edge_slider.sliderReleased.connect(self.image_edge)
        self.reset_button.clicked.connect(self.image_reset)
        self.menuItem1.triggered.connect(self.save_as_image)
        self.OpenItem.triggered.connect(self.get_image_path)
        self.menuItem2.triggered.connect(self.window_translate)
        self.menuItem3.triggered.connect(self.about_message)

        # self.model4_button.clicked.connect(self.coins)

        self.up.clicked.connect(lambda: self.image_scale(0))
        self.down.clicked.connect(lambda: self.image_scale(1))
        self.left.clicked.connect(lambda: self.image_scale(2))
        self.right.clicked.connect(lambda: self.image_scale(3))
        self.reset.clicked.connect(lambda: self.image_scale(4))

    def set_slider(self):
        self.gammar_slider.setMinimum(0)
        self.gammar_slider.setMaximum(100)
        self.gammar_slider.setPageStep(1)
        self.gammar_slider.setValue(50)

        self.binarization_slider.setMinimum(0)
        self.binarization_slider.setMaximum(255)
        self.binarization_slider.setPageStep(1)
        self.binarization_slider.setValue(0)

        self.filter_slider.setMinimum(1)
        self.filter_slider.setMaximum(10)
        self.filter_slider.setPageStep(1)
        self.filter_slider.setValue(1)

        self.edge_slider.setMinimum(0)
        self.edge_slider.setMaximum(100)
        self.edge_slider.setPageStep(1)
        self.edge_slider.setValue(0)

    def get_image_path(self):
        home_dir = str(Path.home())
        self.fname_list = QFileDialog.getOpenFileNames(
            self,
            'Open file',
            home_dir,
            "Image Files (*.png *.jpg *.bmp *.jpeg *.heic)"
        )
        # print(self.fname_list)
        if self.fname_list[0]:
            # return self.fname_list[0]
            print(self.fname_list[0].__len__())
            # self.fname_index = 0
            self.img_path = self.fname_list[0]
            if self.currentImgIdx < 0:
                self.currentImgIdx = 0
            elif self.currentImgIdx >= len(self.img_path):
                self.currentImgIdx = len(self.img_path) - 1
            self.image = QImage(self.img_path[self.currentImgIdx])
            # self.add_image_items()
            # self.image_update()
            self.add_image_items()
            self.loadImage2()
            # self.loadImage()
        else:
            return None

    def update_image(self):
        if self.currentImgIdx < 0:
            self.currentImgIdx = 0
        elif self.currentImgIdx >= len(self.img_path):
            self.currentImgIdx = len(self.img_path) - 1
        self.image = QImage(self.img_path[self.currentImgIdx])
        self.img_pix = QPixmap(self.image)
        self.img_pix = self.img_pix.scaled(
            self.img_label.width(),
            self.img_label.height(),
            Qt.AspectRatioMode.KeepAspectRatio
        )
        self.img_label.setPixmap(self.img_pix)

    def image_update(self):
        self.img_pix = QPixmap(self.image)
        self.img_pix = self.img_pix.scaled(
            self.img_label.width(),
            self.img_label.height(),
            Qt.AspectRatioMode.KeepAspectRatio
        )
        self.img_label.setPixmap(self.img_pix)

    def add_image_items(self):
        for i_p in self.img_path:
            if os.path.isfile(i_p):
                # img_name = os.path.basename(i_p)
                item = QListWidgetItem(QIcon(i_p), '')
                self.imgList.addItem(item)

    def loadImage(self):

        self.currentImgIdx = self.imgList.currentIndex().row()
        self.update_image()

    def loadImage2(self):

        self.currentImgIdx = self.imgList.currentIndex().row()
        self.image_update()

    def resizeEvent(self, event):
        self.image_update()

    def image_gray(self):
        if self.img_path:
            img = cv2.imread(self.img_path[self.currentImgIdx], 1)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            self.image = QtGui.QImage(
                gray.data,
                gray.shape[1],
                gray.shape[0],
                QtGui.QImage.Format.Format_Grayscale8
            )
            self.image_update()

    def image_filter(self):
        if self.img_path:
            img = cv2.imread(self.img_path[self.currentImgIdx])
            src = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            n = self.filter_slider.value()
            blur = cv2.blur(src, (n, n))
            self.image = QtGui.QImage(
                blur.data,
                blur.shape[1],
                blur.shape[0],
                QtGui.QImage.Format.Format_RGB888
            )
            self.image_update()

    def image_binarization(self):
        if self.img_path:
            img = cv2.imread(self.img_path[self.currentImgIdx])
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, binary = cv2.threshold(
                gray,
                self.binarization_slider.value(),
                255,
                cv2.THRESH_BINARY
            )
            self.image = QtGui.QImage(
                binary.data,
                binary.shape[1],
                binary.shape[0],
                QtGui.QImage.Format.Format_Grayscale8
            )
            self.image_update()

    def image_gammar(self):
        if self.img_path:
            img = cv2.imread(self.img_path[self.currentImgIdx])
            slider_value = self.gammar_slider.value()
            if slider_value <= 50:
                gamma = 1 - ((50 - slider_value) * 0.02)
            else:
                gamma = 1 + 0.2 * slider_value

            gamma_table = [np.power(x / 255.0, gamma) * 255.0 for x in range(256)]  # 建立映射表
            gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)
            gamma_image = cv2.LUT(img, gamma_table)
            self.image = QtGui.QImage(
                gamma_image.data,
                gamma_image.shape[1],
                gamma_image.shape[0],
                QtGui.QImage.Format.Format_BGR888
            )
            self.image_update()

    def image_edge(self):
        if self.img_path:
            img = cv2.imread(self.img_path[self.currentImgIdx], 0)
            edge = cv2.Canny(img, 100, self.edge_slider.value() * 8)
            self.image = QtGui.QImage(
                edge.data,
                edge.shape[1],
                edge.shape[0],
                QtGui.QImage.Format.Format_Grayscale8
            )
            self.image_update()

    # def coins(self):
        # if self.img_path:
        #     # Read the image file using OpenCV
        #     img = cv2.imread(self.img_path[self.currentImgIdx], 0)
        #     # Convert the image to grayscale
        #     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #     self.image = QtGui.QImage(
        #         gray.data,
        #         gray.shape[1],
        #         gray.shape[0],
        #         QtGui.QImage.Format.Format_Grayscale8
        #     )
        #     # 使用阈值进行二值化处理
        #     ret, binary = cv2.threshold(
        #         gray,
        #         self.binarization_slider.value(),
        #         255,
        #         cv2.THRESH_BINARY
        #     )
        #     # thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        #     # 检测图像中的圆形
        #     circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 100, param1=100, param2=50, minRadius=10,
        #                                maxRadius=100)
        #     self.image = QtGui.QImage(
        #         gray.data,
        #         gray.shape[1],
        #         gray.shape[0],
        #         QtGui.QImage.Format.Format_Grayscale8
        #     )
        #     self.image_update()
        #     # 绘制圆形
        #     if circles is not None:
        #         circles = np.round(circles[0, :]).astype("int")
        #         for (x, y, r) in circles:
        #             cv2.circle(img, (x, y), r, (0, 255, 0), 4)
        #
        #     # 统计圆形的数量
        #     coin_count = 0
        #     if circles is not None:
        #         coin_count = len(circles)
        #         circles = np.round(circles[0, :]).astype("int")
        #         for (x, y, r) in circles:
        #             cv2.circle(img, (x, y), r, (0, 255, 0), 4)
        #
        #     # 显示统计结果
        #     print('Coin count:', coin_count)
        #
        # img = cv2.imread(self.img_path[self.currentImgIdx], 0)
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        # contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #
        # coin_count = 0
        # for contour in contours:
        #     area = cv2.contourArea(contour)
        #     if area > 100:
        #         coin_count += 1
        #
        # box = QMessageBox()
        # box.setText("The value is %d" % coin_count)
        # box.exec()


    def image_reset(self):
        self.image = QImage(self.img_path[self.currentImgIdx])
        self.update_image()
        self.set_slider()

    def window_translate(self):
        self.is_cn = not self.is_cn
        if self.is_cn:
            self.retranslateUi(self)
        else:
            self.retranslateUi_en(self)

    def save_image(self):
        if self.img_path != '':
            suffix = self.img_path.split(".")[1]
            self.image.save(self.img_path, suffix, 100)

    def save_as_image(self):
        file_dir = os.path.dirname(self.img_path[self.currentImgIdx])
        file_path = QFileDialog.getSaveFileName(
            self,
            "保存文件",
            file_dir,
            "Image Files (*.png *.jpg *.bmp *.jpeg)"
        )
        if file_path[0]:
            suffix = file_path[0].split(".")[1]
            self.image.save(file_path[0], suffix, 100)

    # def resizeEvent(self, event):
    #     self.update_image()

    def image_scale(self, mode):
        if self.img_path:
            image = cv2.imread(self.img_path[self.currentImgIdx])
            img = image
            if mode == 4:
                self.image_reset()
                return
            elif mode == 0:
                img = cv2.flip(image, 0)
            elif mode == 1:
                img = cv2.flip(image, 0)
            elif mode == 2:
                img = cv2.flip(image, 1)
            elif mode == 3:
                img = cv2.flip(image, 1)
            self.image = QtGui.QImage(
                img.data,
                img.shape[1],
                img.shape[0],
                QtGui.QImage.Format.Format_BGR888
            )
            self.image_update()

    # def img_scale(self, mode):
    #     if self.img_path:
    #         image = cv2.imread(self.img_path[self.currentImgIdx])
    #         img = image
    #         if mode == 4:
    #             self.image_update()
    #             return
    #         elif mode == 0:
    #             img = cv2.flip(image, 1)
    #         elif mode == 1:
    #             img = cv2.flip(image, 0)
    #         elif mode == 2:
    #             img = cv2.flip(image, 1)
    #         elif mode == 3:
    #             img = cv2.flip(image, 1)
    #         self.image = QtGui.QImage(
    #             img.data,
    #             img.shape[1],
    #             img.shape[0],
    #             QtGui.QImage.Format.Format_BGR888
    #         )
    #         self.image_update()

    @staticmethod
    def about_message():
        message = QMessageBox()
        message.setText("本软件由209050318刘滨榕开发")
        message.setWindowTitle("关于本软件")
        message.exec()

    def retranslateUi_en(self, MainWidget):
        _translate = QtCore.QCoreApplication.translate
        MainWidget.setWindowTitle(_translate("MainWidget", "Simple ImagesProcess by 209050318lbr"))
        self.gammar_label.setText(_translate("MainWidget", "Gamma"))
        self.gray_button.setText(_translate("MainWidget", "Gray"))
        self.binarization_label.setText(_translate("MainWidget", "Binarization"))
        self.fliter_label.setText(_translate("MainWidget", "Filter"))
        self.edge_label.setText(_translate("MainWidget", "Edge"))
        self.reset_button.setText(_translate("MainWidget", "ResetImages"))
        self.exitButton.setText(_translate("MainWidget", "Exit"))
        self.vidButton.setText(_translate("MainWidget", "VideoProcess"))
        self.OpenItem.setText(_translate("MainWidget","open files"))
        self.menuItem1.setText(_translate("MainWidget","save image as..."))
        self.menuItem2.setText(_translate("MainWidget", "translate all widget"))
        self.menuItem3.setText(_translate("MainWidget", "about app"))
        self.file_button.setText(_translate("VideoProcess", "File"))
        self.func_button.setText(_translate("VideoProcess", "Function"))
        self.info_button.setText(_translate("VideoProcess", "Information"))
        # self.model4_button.setText(_translate("MainWidget", "Activate Coins-Detective"))

    # def coins_from_shine(self):
    #     image_data = self.image.bits()
    #     image = cv2.UMat(image_data)
    #     image = cv2.imdecode(image, cv2.IMREAD_UNCHANGED)
    #     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #     blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    #     circles = cv2.HoughCircles(
    #         blurred,
    #         cv2.HOUGH_GRADIENT,
    #         dp=1,
    #         minDist=100,
    #         param1=100,
    #         param2=30,
    #         minRadius=30,
    #         maxRadius=100
    #     )
    #     for circle in circles[0]:
    #         x, y, r = circle
    #         cv2.circle(image, (x, y), r, (0, 0, 255), 2)
    #         cv2.imshow('coins', image)


class video_Func(QWidget, Ui_VideoProcess):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.img_path = ['', '']
        self.image = QImage(self.img_path[0])
        self.img_pix = None
        self.currentImgIdx = 0
        self.currentImg = None
        self.img_path_str = ''

        self.video_path = ''

        self.camera_model = 0
        self.timer_camera = QtCore.QTimer()  # 初始化定时器
        self.cap = cv2.VideoCapture()  # 初始化摄像头
        self.CAM_NUM = 0
        self.CAM_SIGNAL = 0
        self.__flag_work = 0
        self.is_cn = True
        self.init_ui()


    def init_ui(self):
        self.set_slot()

    def set_slot(self):
        self.model0_button.clicked.connect(lambda: self.set_cameramodel(0))
        self.model2_button.clicked.connect(lambda: self.set_cameramodel(2))
        self.model1_button.clicked.connect(lambda: self.set_cameramodel(1))
        self.mode3_button.clicked.connect(lambda: self.set_cameramodel(3))
        self.model4_button.clicked.connect(lambda: self.set_cameramodel(4))
        self.timer_camera.timeout.connect(lambda: self.show_camera())
        self.menuItem1.triggered.connect(self.save_as_image)
        self.menuItem2.triggered.connect(self.widget_translate)
        self.menuItem3.triggered.connect(self.about_message)

    def get_image_path(self):
        home_dir = str(Path.home())
        fname = QFileDialog.getOpenFileName(
            self,
            'Open file',
            home_dir,
            "Image Files (*.png *.jpg *.bmp *.jpeg)"
        )
        print(fname)
        if fname[0]:
            self.img_path = fname[0]
            self.image = QImage(self.img_path)
            self.update_image()

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

    def update_image(self):
        self.img_pix = QPixmap(self.image)
        self.img_pix = self.img_pix.scaled(
            self.img_label.width(),
            self.img_label.height(),
            Qt.AspectRatioMode.KeepAspectRatio
        )
        self.img_label.setPixmap(self.img_pix)

    def open_camera(self):
        self.img_path = ['', '']
        if not self.timer_camera.isActive():
            flag = self.cap.open(self.CAM_NUM)
            if not flag:
                QtWidgets.QMessageBox.Warning(self, u'Warning', u'请检测相机与电脑是否连接正确',
                                              buttons=QtWidgets.QMessageBox.StandardButton.Ok,
                                              defaultButton=QtWidgets.QMessageBox.StandardButton.Ok)
            else:
                self.timer_camera.start(30)
        else:
            self.timer_camera.stop()
            self.cap.release()
            self.img_label.clear()

    def show_camera(self):
        flag, image_read = self.cap.read()
        show = cv2.cvtColor(image_read, cv2.COLOR_BGR2RGB)
        if self.camera_model == 0:
            self.image = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format.Format_RGB888)

        elif self.camera_model == 1:
            gray = cv2.cvtColor(image_read, cv2.COLOR_BGR2GRAY)
            show = cv2.Canny(gray, 100, 150)
            self.image = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format.Format_Grayscale8)

        elif self.camera_model == 2:
            gray = cv2.cvtColor(image_read, cv2.COLOR_BGR2GRAY)
            ret, show = cv2.threshold(
                gray,
                127,
                255,
                cv2.THRESH_BINARY
            )
            self.image = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format.Format_Grayscale8)

        elif self.camera_model == 3:
            show = cv2.cvtColor(image_read, cv2.COLOR_BGR2GRAY)
            self.image = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format.Format_Grayscale8)

        elif self.camera_model == 4:
            # Convert the image to grayscale
            gray = cv2.cvtColor(image_read, cv2.COLOR_BGR2GRAY)

            # Use Gaussian blur to smooth the image
            blur = cv2.GaussianBlur(gray, (5, 5), 0)

            # Use the Canny edge detector to find the edges in the image
            edges = cv2.Canny
            self.image = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format.Format_Grayscale8)
        self.update_image()

    def set_cameramodel(self, model):
        self.camera_model = model
        self.open_camera()

    def save_image(self):
        self.img_path_str = ''.join(self.img_path)
        if self.img_path_str != '':
            suffix = self.img_path_str.split(".")[1]
            self.image.save(self.img_path, suffix, 100)

    def save_as_image(self):
        self.img_path_str= ''.join(self.img_path)
        file_dir = os.path.dirname(self.img_path_str)
        file_path = QFileDialog.getSaveFileName(
            self,
            "保存文件",
            file_dir,
            "Image Files (*.png *.jpg *.bmp *.jpeg)"
        )
        if file_path[0]:
            suffix = file_path[0].split(".")[1]
            self.image.save(file_path[0], suffix, 100)

    def widget_translate(self):
        self.is_cn = not self.is_cn
        if self.is_cn:
            self.retranslateUi(self)
        else:
            self.retranslateUi_en(self)

    def retranslateUi_en(self, MainWidget):
        _translate = QtCore.QCoreApplication.translate
        MainWidget.setWindowTitle(_translate("MainWindow", "VideoProcess by lbr"))
        self.img_button.setText(_translate("VideoProcess", "ImgProcess"))
        self.exit_button.setText(_translate("VideoProcess", "Exit"))
        self.file_button.setText(_translate("VideoProcess", "File"))
        self.func_button.setText(_translate("VideoProcess", "Function"))
        self.info_button.setText(_translate("VideoProcess", "Information"))
        self.model0_button.setText(_translate("VideoProcess", "Activate Camera"))
        self.model1_button.setText(_translate("VideoProcess", "Activate Edge-Camera"))
        self.model2_button.setText(_translate("VideoProcess", "Activate Bio-Camera"))
        self.mode3_button.setText(_translate("VideoProcess", "Activate Graied-Camera"))
        # self.model4_button.setText(_translate("VideoProcess", "启用硬币检测"))

    @staticmethod
    def about_message():
        message = QMessageBox()
        message.setText(
            "本软件由209050318刘滨榕开发")
        message.setWindowTitle("关于本软件")
        message_icon = QPixmap("image/about.jpg")
        message_icon = message_icon.scaled(
            100,
            100,
            Qt.AspectRatioMode.KeepAspectRatio
        )
        message.setIconPixmap(message_icon)
        message.exec()

