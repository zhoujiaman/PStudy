# -*- coding: utf-8 -*-
import os
import sys
import string
from PyQt4 import QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import camera
import threading
from datetime import datetime

class PyQtButton(QtGui.QWidget):
    def __init__(self, *args):
        super(QtGui.QWidget, self).__init__()
        self.initUI()

        self.video = camera.camera(self.cameraLabel)
        self.video.start()

    def initUI(self, *args):
        # title
        self.setWindowTitle('Fun-Camera')
        self.color=QtGui.QColor(255,255,255)
        self.setStyleSheet('QWidget{background-color:%s}'%self.color.name())

        layout = QtGui.QGridLayout(self)
        # camera label
        self.cameraLabel = QtGui.QLabel(self);
        self.cameraLabel.setPixmap(QPixmap('./pic/loading.gif'))
	    self.movie = QtGui.QMovie('./pic/loading.gif')
	    self.cameraLabel.setMovie(self.movie)
	    self.movie.start()
        self.cameraLabel.setFixedWidth(500)
        self.cameraLabel.setFixedHeight(500)
        self.cameraLabel.setAlignment(Qt.AlignCenter)
        self.cameraLabel.setScaledContents(True)
        layout.addWidget(self.cameraLabel,1,0,8,1)

        # preview
        self.preLabel = QtGui.QLabel(self);
        self.preLabel.setPixmap(QPixmap('./sticker/cat.png'))
        self.preLabel.setFixedWidth(200)
        self.preLabel.setFixedHeight(200)
        self.preLabel.setAlignment(Qt.AlignCenter)
        self.preLabel.setScaledContents(True)
        layout.addWidget(self.preLabel,1,1,4,3)

        # right sticker button
        names = ('./sticker/cat.png',
                 './sticker/shy.png',
                 './sticker/ear.png',
                 './sticker/glasses.png',
                 './sticker/horrible.png',
                 './sticker/terror.png',)
        for i, name in enumerate(names):
            self.button = QtGui.QPushButton(self)
            self.button.setIcon(QIcon(name))
            self.button.setStyleSheet('''QPushButton{background-color:white;border:2px solid gray;border-radius:10px;}''')
            self.button.setFixedWidth(50)
            self.button.setFixedHeight(50)
	    name_dot = name.split('.')
	    name_line = name_dot[1].split('/')
            self.button.clicked.connect(self.preSticker(name,name_line[2]))
            if i <3 :
                layout.addWidget(self.button, 4, i + 1, 2, 1)
            else:
                layout.addWidget(self.button, 5, i-2, 2, 1)

        # take photos button
        takeButton = QtGui.QPushButton('take photos')
        takeButton.setStyleSheet('''QPushButton{background-color:white;border:2px solid gray;border-radius:10px;}''')
        takeButton.setFixedWidth(120)
        takeButton.setFixedHeight(40)
        takeButton.clicked.connect(self.screenShot)

        # help button
        helpButton = QtGui.QPushButton('Help')
        helpButton.setStyleSheet('''QPushButton{background-color:white;border:2px solid gray;border-radius:10px;}''')
        helpButton.setFixedWidth(60)
        helpButton.setFixedHeight(40)
        helpButton.clicked.connect(self.showHelp)

        # add to layout
        layout.addWidget(takeButton,7,1,1,2)
        layout.addWidget(helpButton,8,5,1,1)
        self.setGeometry(300, 300, 350, 300)
        self.setLayout(layout)

    def preSticker(self, stickerPath, stickerTitle):
        def callpreview():
	    #self.preSticker = '';
	    if self.preSticker != stickerTitle:
		self.preLabel.setPixmap(QPixmap(stickerPath))
		self.video.setWelts([''+stickerTitle+''])
		self.preSticker = stickerTitle
	    else:
		#self.preLabel.setPixmap(QPixmap(''))
		self.video.setWelts([])
		self.preSticker = ''
        return callpreview

    def showHelp(self):
        super(QtGui.QWidget, self).__init__()
        self.setWindowTitle('Fun-Camera Help')
        self.setStyleSheet('QWidget{background-color:%s}'%self.color.name())

        helpLayout = QtGui.QGridLayout(self)

        # introduce and first tips
        self.introduceLabel = QtGui.QLabel(self);
        self.introduceLabel.setText('Welcome to the fun-camera! Here you can record all your unforgettable moments.\nNext, please allow me to introduce the software!\n1.')
	self.introduceLabel.setFont(QFont("黑体",20))
        helpLayout.addWidget(self.introduceLabel, 0, 0, 1, 1)

        # start image label
        self.helpLabel = QtGui.QLabel(self);
        self.helpLabel.setPixmap(QPixmap('./pic/start.png'))
        self.helpLabel.setFixedWidth(400)
        self.helpLabel.setFixedHeight(400)
        self.helpLabel.setAlignment(Qt.AlignCenter)
        self.helpLabel.setScaledContents(True)
        helpLayout.addWidget(self.helpLabel, 1, 0, 1, 1)

        # second tips
        self.twoTipsLabel = QtGui.QLabel(self);
        self.twoTipsLabel.setText('2.')
	self.twoTipsLabel.setFont(QFont("黑体",20))
        helpLayout.addWidget(self.twoTipsLabel, 2, 0, 1, 1)

        # take image label
        self.takeLabel = QtGui.QLabel(self);
        self.takeLabel.setPixmap(QPixmap('./pic/take.png'))
        self.takeLabel.setFixedWidth(400)
        self.takeLabel.setFixedHeight(400)
        self.takeLabel.setAlignment(Qt.AlignCenter)
        self.takeLabel.setScaledContents(True)
        helpLayout.addWidget(self.takeLabel, 5, 0, 1, 1)

        # third and fourth tips
        self.thirdFourthTipsLabel = QtGui.QLabel(self);
        self.thirdFourthTipsLabel.setText('3. Whenever you want to see this instruction, you can click the button "Help". \n4. This is the manual of the software. Wish all of you have a good time!')
	self.thirdFourthTipsLabel.setFont(QFont("黑体",20))
        helpLayout.addWidget(self.thirdFourthTipsLabel, 6, 0, 1, 1)

        self.setLayout(helpLayout)
        self.show()

    # screenshot method
    def screenShot(self):
        date = datetime.now()
        filename = date.strftime('%Y-%m-%d_%H-%M-%S.jpg')

        screenshot = QPixmap.grabWindow(self.winId(),x=10, y=10, width=500,height=500)
        # screenshot image savepath
        screenshot.save(os.path.expanduser("~/screenshot/"+filename), "jpg")

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    tb = PyQtButton()
    tb.show()
    app.exec_()
