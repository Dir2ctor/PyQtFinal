import sys

from PyQt6 import QtWidgets

from mainwidget_ui import Ui_MainWidget

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWidget()
    ui.show()
    sys.exit(app.exec())

