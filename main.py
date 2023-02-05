import os
import sys

import requests

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.getImage(self.createurl())
        self.print_img(self.map_file)
        self.zum = 17
        self.scale.setText(f'Маcштаб {str(self.zum)}')

    def print_img(self, name):
        self.pixmap = QPixmap(name)
        self.mapp.setPixmap(self.pixmap)

    def run(self):
        print(1)

    def initUI(self):
        # self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        ## Изображение
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def createurl(self, z=17):
        return f"http://static-maps.yandex.ru/1.x/?ll=37.530887,55.703118&z={z}&l=map&size=650,450"

    def getImage(self, map_request):
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_PageUp:
            self.scale_map(1)
        elif key == Qt.Key_PageDown:
            self.scale_map(0)

    def scale_map(self, main):
        if main and self.zum < 17:
            self.zum += 1
        if not main and self.zum > 0:
            self.zum -= 1
        self.getImage(self.createurl(self.zum))
        self.print_img(self.map_file)
        self.scale.setText(f'Маcштаб {str(self.zum)}')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MyWidget()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
