import sys

from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Paint(QMainWindow):
    def __init__(self):
        super().__init__()

        QToolTip.setFont(QFont('SansSerif', 10))

        self.setWindowTitle("Paint")
        self.setGeometry(100, 100, 1000, 800)
        self.setWindowIcon(QIcon('Paint_Windows_8_icon.png'))

        self.resizeSavedImage = QImage(0, 0, QImage.Format_RGB32)
        self.savedImage = QImage(0, 0, QImage.Format_RGB32)

        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        # Переменные
        self.drawing = False
        self.brushSize = 2
        self.brushColor = Qt.black

        self.lastPoint = QPoint()
        mainMenu = self.menuBar()

        # Добавление строки "Файл"
        fileMenu = mainMenu.addMenu("Файл")

        # Добавление кисти
        b_size = mainMenu.addMenu("Размер кисти")
        b_color = mainMenu.addMenu("Цвет")

        # Добавление справки
        infoMenu = mainMenu.addMenu("Справка")

        # Установка размера кисти
        pix = QAction("4px", self)
        b_size.addAction(pix)
        pix.triggered.connect(self.Pixel_4)

        # Установка цвета кисти
        black = QAction("Чёрный", self)
        b_color.addAction(black)
        black.triggered.connect(self.blackColor)

    # Проверка нажатия на левую кнопку мыши и установка позиции курсора, если нажаите произошло
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

    # Контроль движения мыши, отрисовка маршрута и сохранение последней позиции
    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brushColor, self.brushSize,
                                Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

    # Контроль отпускания левой кнопки мыши
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    # Обработчик перерисовки виджета
    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

    # Функция, вызывающая окно с сообщением для подтверждения действия
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Сообщение',
                                     "Вы действительно хотите выйти?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # Функция, центрирующая окно на рабочем столе
    def center(self):

        place = self.frameGeometry()
        monitor_size = QDesktopWidget().availableGeometry().center()
        place.moveCenter(monitor_size)
        self.move(place.topLeft())

    def Pixel_4(self):
        self.brushSize = 4

    def blackColor(self):
        self.brushColor = Qt.black

# Создание pyQt5 app
App = QApplication(sys.argv)

# Создание экземпляра окна
paint = Paint()

paint.show()

# Запуск app
sys.exit(App.exec())