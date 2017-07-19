# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import cv2
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PIL import Image
import time

class camera(QtGui.QWidget):
	"""docstring for camera"""

	ANTI_VIBRATION = 15

	FPS_COUNT_LOOP = 30

	fps_counter = 0

	pre_frames = []

	welts = {
	    'ear': {'img': './sticker/ear.png', 'offset_y': 20},
	    'glasses': {'img': './sticker/glasses.png', 'offset_y': 85},
		'cat': {'img': './sticker/cat.png', 'offset_y': 90},
		'horrible': {'img': './sticker/horrible.png', 'offset_y': 90},
		'shy': {'img': './sticker/shy.png', 'offset_y': 90},
		'terror': {'img': './sticker/terror.png', 'offset_y': 90},
	}

	enabled_welt_names = []

	welts_imread = []

	def __init__(self, cameraLabel):
		super(QtGui.QWidget, self).__init__()
		#self.setWelts(['glasses'])
		self.cap = cv2.VideoCapture('test.mp4')
		self.face_cascade = cv2.CascadeClassifier('./xml/haarcascade_frontalface_default.xml')
		self.video_frame = cameraLabel


	def setWelts(self, list):
		self.enabled_welt_names = list
		self.welts_imread = []
		#if list != '':
		for i in self.enabled_welt_names:
			config = self.welts[i]
			self.welts_imread.append([
				cv2.imread(config['img'], cv2.IMREAD_UNCHANGED),
				config['offset_y']
			])

	def start(self):
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.nextFrameSlot)
		self.timer.start(50)

	def nextFrameSlot(self):
		ret, frame = self.cap.read()
		if not ret:
			return
		self.locate(frame, self.face_cascade)
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		img = QtGui.QImage(frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
		pix = QtGui.QPixmap.fromImage(img)
		self.video_frame.setPixmap(pix)

	def locate(self, frame, face_cascade):
	    if self.fps_counter%self.FPS_COUNT_LOOP == 0:
	        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	    else:
	        faces = self.pre_frames

	    #print pre_frames
	    self.fps_counter += 1
	    i = 0
	    if len(faces) > 0 and len(self.pre_frames) > len(faces):
	        self.pre_frames = self.pre_frames[0:len(faces)]

	    #print pre_frames
	    #print self.enabled_welt_names
	    for (x,y,w,h) in faces:
	        #print '------hit'
	        #cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
	        if i < len(self.pre_frames):
	            (_x, _y, _w, _h) = self.pre_frames[i]
	            max_ati = max(abs(_x-x), abs(_y-y) , abs(_w-w), abs(_h-h))
	            #print max_ati
	            #print max_ati < anti_vibration
	            if max_ati < self.ANTI_VIBRATION:
	                x = _x
	                y = _y
	                w = _w
	                h = _h
	            else:
	                self.pre_frames[i] = [x,y,w,h]
	        else:
	            self.pre_frames.append([x,y,w,h])
	        i = i + 1

	        #print self.welts_imread
	        for (welt, offset_y) in self.welts_imread:
		        #print (x,y,w,h)
		        welt_d = cv2.resize(welt, (w, int((w / welt.shape[1]) * welt.shape[0])))
		        ww = welt_d.shape[1]
		        wh = welt_d.shape[0]
		        wx = x;
		        wy = int(y + (offset_y / 100) * h - wh);
		        if wy < 0:
		            welt_d = welt_d[-wy: wh, :ww]
		            wy = 0
		            wh = welt_d.shape[0]

		        for c in range(0,3):
		            frame[wy:wy+wh, wx:wx+ww, c] = welt_d[:,:,c] * (welt_d[:,:,3]/255.0) +  frame[wy:wy+wh, wx:wx+ww, c] * (1.0 - welt_d[:,:,3]/255.0)
