import sys

from PyQt6.QtWidgets import QApplication

from MainWindow import MainWindow
from Model import Model
from Controller import Controller


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    model = Model()
    controller = Controller(model, window)
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()