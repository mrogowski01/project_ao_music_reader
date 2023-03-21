from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class Image(QWidget):
    def  __init__(self, src, width, height):
        super(Image, self).__init__()
        pixmap = QPixmap(src)
        self.label = QLabel(self)
        self.label.setMargin(0)
        # self.label.setScaledContents(True) # do skalowania
        self.label.resize(width, height)
        # self.label.setStyleSheet("background-color: blue")
        self.label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)

        if src != '': self.label.setPixmap(pixmap)#.scaled(width, 400, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def setImage(self, src, width):
        self.label.clear()
        pixmap = QPixmap(src)
        self.label.setPixmap(pixmap.scaledToWidth(width - 60, mode=Qt.TransformationMode.SmoothTransformation))

    def getLabel(self):
        return self.label