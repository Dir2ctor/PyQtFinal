import sys

from PyQt6 import QtWidgets

from func import Func, video_Func
from mainwidget_ui import Ui_MainWidget
from auto_video_ui import Ui_VideoProcess


def switch_ui1(m: Ui_MainWidget, i: Func):
    m.close()
    i.img_path = m.get_image_path()
    if i.img_path is not None:
        i.update_image()
        i.add_image_items()
        i.show()
    else:
        m.show()
def switch_ui2(i:Func, v:video_Func):
    i.close()
    v.show()
def switch_ui3(m:Ui_MainWidget, v:Func):
    m.close()
    v.show()
def switch_ui4(v:video_Func, i:Func):
    v.close()
    i.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    m = Ui_MainWidget()
    m.show()
    i = Func()
    v = video_Func()
    m.pushButton.clicked.connect(lambda: switch_ui1(m, i))
    m.pushButton_2.clicked.connect(lambda: switch_ui3(m,v))
    i.vidButton.clicked.connect(lambda:switch_ui2(i,v))
    v.img_button.clicked.connect(lambda:switch_ui4(v,i))
    sys.exit(app.exec())
