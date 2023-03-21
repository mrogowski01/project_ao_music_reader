from PyQt6.QtWidgets import QMainWindow, QWidget, QSpinBox, QHBoxLayout, QVBoxLayout, QFileDialog
from GUI.Button import Button
from GUI.Image import Image
from GUI.Color import Color #dev
from Music.Audio import Audio
from Music.Notes import Notes
import threading
import sys

#from .. import pozycje_obiektow

import sys

# appending the parent directory path
sys.path.append('..')

# importing the methods
from pozycje_obiektow import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Music reader")
        self.resize(1000, 600)
        self.windowWidth = self.frameGeometry().width()
        self.windowHeight = self.frameGeometry().height()
        self.readImage = Image('', int(1000 * .42), self.windowHeight)
        self.p = Audio()
        self.notes = []
        self.fileName = ""

        # print(self.frameGeometry().width())
        # self.setGeometry(100, 100, 600, 400)

        # self.setCentralWidget(button)
        layout = QHBoxLayout()

        layout.addWidget(self.readImage, 40)
        layout.addWidget(Color('gray'), 40)

        menuLayout = QVBoxLayout()
        btn = Button("Load image", self.loadImage)
        menuLayout.addWidget(btn)

        self.algorithmButton = Button("Make an ALG!", self.tempAlg)
        self.algorithmButton.setEnabled(False)
        menuLayout.addWidget(self.algorithmButton)

        self.playMusicButton = Button("Play", self.playMusic)
        self.playMusicButton.setEnabled(False)
        menuLayout.addWidget(self.playMusicButton)

        self.stopMusicButton = Button("Stop", self.stopMusic)
        self.stopMusicButton.setEnabled(False)
        menuLayout.addWidget(self.stopMusicButton)

        self.rate = QSpinBox()
        self.rate.setMinimum(60)
        self.rate.setMaximum(180)
        self.rate.setValue(120)

        menuLayout.addWidget(self.rate)
        # self.rate.valueChanged.connect(self.rateChanged)


        btn = Button("Close application", self.close)
        menuLayout.addWidget(btn)
        menuLayout.addStretch()

        layout.addLayout(menuLayout)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.show()

    # def rateChanged(self, i):
        # print(f'Rate changed to {i}')

    def tempAlg(self):
        print("Im doing something with photo and after that...")
        self.notes = generate_notes(self.fileName)
        self.playMusicButton.setEnabled(True)

    def closeEvent(self, event):
        try:
            self.stopMusic()
        except:
            print("No music is playing")
        finally:
            sys.exit()

    def loadImage(self):
        fname = QFileDialog.getOpenFileName(self, "Open file", "${HOME}", "PNG Files (*.png);; JPG Files(*.jpg)")
        print(f'Loading image {fname[0]}')
        if fname[0] != '':
            self.readImage.setImage(fname[0], 500)
            self.fileName = fname[0]
            self.algorithmButton.setEnabled(True) # after reading notes

    def playMusic(self):
        # print("I'm playing the music")
        
        self.playMusicButton.setEnabled(False)
        self.stopMusicButton.setEnabled(True)
        #notes = ["E4", "E4", "E4", "E4", "E4", "E4", "-", "E4", "G4", "C4", "D4", "E4"]
        #durations = [Notes.QUARTER_NOTE, Notes.QUARTER_NOTE, Notes.HALF_NOTE, Notes.QUARTER_NOTE, Notes.QUARTER_NOTE, Notes.HALF_NOTE, Notes.HALF_NOTE, Notes.QUARTER_NOTE, Notes.QUARTER_NOTE, Notes.QUARTER_NOTE, Notes.QUARTER_NOTE, Notes.WHOLE_NOTE]
        durations = [Notes.QUARTER_NOTE for i in range(len(self.notes))]
        self.p.set(self.notes, durations)
        self.p.play(self.playMusicButton, self.stopMusicButton, self.rate.value())

    def stopMusic(self):
        self.p.stop()
        self.playMusicButton.setEnabled(True)
        self.stopMusicButton.setEnabled(False)
