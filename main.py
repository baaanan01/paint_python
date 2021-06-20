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

        # Возможность выбора разной толщины кисти
        pix = QAction("4px", self)
        b_size.addAction(pix)
        pix.triggered.connect(self.Pixel_4)

        pix_8 = QAction("8px", self)
        b_size.addAction(pix_8)
        pix_8.triggered.connect(self.Pixel_8)

        pix_12 = QAction("12px", self)
        b_size.addAction(pix_12)
        pix_12.triggered.connect(self.Pixel_12)

        pix_14 = QAction("14px", self)
        b_size.addAction(pix_14)
        pix_14.triggered.connect(self.Pixel_14)

        pix_16 = QAction("16px", self)
        b_size.addAction(pix_16)
        pix_16.triggered.connect(self.Pixel_16)

        pix_32 = QAction("32px", self)
        b_size.addAction(pix_32)
        pix_32.triggered.connect(self.Pixel_32)

        pix_64 = QAction("64px", self)
        b_size.addAction(pix_64)
        pix_64.triggered.connect(self.Pixel_64)

        pix_72 = QAction("72px", self)
        b_size.addAction(pix_72)
        pix_72.triggered.connect(self.Pixel_72)

        #Выборка различных цветов кисти
        black = QAction("Чёрный", self)
        b_color.addAction(black)
        black.triggered.connect(self.blackColor)

        yellow = QAction("Жёлтый", self)
        b_color.addAction(yellow)
        yellow.triggered.connect(self.yellowColor)

        red = QAction("Красный", self)
        b_color.addAction(red)
        red.triggered.connect(self.redColor)

        white = QAction("Белый", self)
        b_color.addAction(white)
        white.triggered.connect(self.whiteColor)

        green = QAction("Зеленый", self)
        b_color.addAction(green)
        green.triggered.connect(self.greenColor)

        # Добавляем О нас
        aboutAction = QAction("О нас", self)
        # Добавляем подраздел "О нас" в меню Справка
        infoMenu.addAction(aboutAction)
        # Шорткат
        aboutAction.setShortcut("Ctrl+I")
        # Когда мы нажимаем на Справка->О нас, триггерится функция about
        aboutAction.triggered.connect(self.about)

        # Создание опции "Сохранить"
        saveAction = QAction("Сохранить как...", self)
        saveAction.setShortcut("Ctrl + S")
        fileMenu.addAction(saveAction)
        saveAction.triggered.connect(self.save)

        # Очистка
        clearAction = QAction("Очистить", self)
        clearAction.setShortcut("Ctrl + C")
        fileMenu.addAction(clearAction)
        clearAction.triggered.connect(self.clear)

        #Выход
        exitAction = QAction("Выход", self)
        exitAction.setShortcut("Ctrl+Q")
        fileMenu.addAction(exitAction)
        exitAction.triggered.connect(self.exitProgram)

        # Создание опции приближения

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

    # Функция, сохраняющая изображение
    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Сохранить", "",
                                                  "PNG(*.png);;JPEG(*.jpg *.jpeg);;Монохромный рисунок(*.bmp *.dib);;"
                                                  "TIFF(*.tif *.tiff);;All Files(*.*) ")
        if filePath == "":
            return
        self.image.save(filePath)

    # Функция, центрирующая окно на рабочем столе
    def center(self):

        place = self.frameGeometry()
        monitor_size = QDesktopWidget().availableGeometry().center()
        place.moveCenter(monitor_size)
        self.move(place.topLeft())

    # Очистка всего поля
    def clear(self):
        self.image.fill(Qt.white)
        self.update()

    def about(self):
        msg = QMessageBox()
        msg.setText("<p>Над программой работали: Беличенко Дарья, Строкач Никита</p>"
                    "<p>БСБО-04-19</p>")
        msg.setWindowTitle("О нас")
        msg.exec_()

    def exitProgram(self):
        QtCore.QCoreApplication.quit()

    def blackColor(self):
        self.brushColor = Qt.black

    def yellowColor(self):
        self.brushColor = Qt.yellow

    def redColor(self):
        self.brushColor = Qt.red

    def whiteColor(self):
        self.brushColor = Qt.white

    def greenColor(self):
        self.brushColor = Qt.green

    def Pixel_4(self):
        self.brushSize = 4

    def Pixel_8(self):
        self.brushSize = 8

    def Pixel_12(self):
        self.brushSize = 12

    def Pixel_14(self):
        self.brushSize = 14

    def Pixel_16(self):
        self.brushSize = 16

    def Pixel_32(self):
        self.brushSize = 32

    def Pixel_64(self):
        self.brushSize = 64

    def Pixel_72(self):
        self.brushSize = 72

# Создание pyQt5 app
App = QApplication(sys.argv)

# Создание экземпляра окна
paint = Paint()

paint.show()

# Запуск app
sys.exit(App.exec())