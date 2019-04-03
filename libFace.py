import time, datetime
import imutils
import cv2
import numpy as np
import serial,io
import socket  # Import socket module
import picamera
from picamera.array import PiRGBArray

class PICam:
    def __init__(self, videofile="", size=(1920, 1080), rotate=0, vflip=False, hflip=False):
        self.camsize = size
        self.fps = 0
        self.frameID = 0
        self.start_time = 0

        if(len(videofile)>0):
            self.cam = cv2.VideoCapture(videofile)
            self.playvideo = True
        else:
            self.cam = picamera.PiCamera()
            self.size = size
            self.rawCapture = PiRGBArray(self.cam)
            self.cam.resolution = size
            self.cam.brightness = 60
            self.cam.vflip = vflip
            self.cam.hflip = hflip
            self.cam.rotation = rotate
            self.playvideo = False

    def working(self):
        return True

    def getFrame(self):
        camera = self.cam
        #camera.framerate = 32
        rawCapture = self.rawCapture
        rawCapture.truncate(0)
        #time.sleep(0.1)
        camera.capture(rawCapture, format="bgr")
        image = rawCapture.array
        image = image[:,:,::-1]
        #print(image.shape)

        if(self.frameID == 0):
            self.start_time = time.time()
        else:
            self.fps = self.frameID / (time.time() - self.start_time)

        self.frameID += 1


        return True, image


class webCam:
    def __init__(self, id=0, videofile="", size=(1920, 1080)):
        self.camsize = size
        self.fps = 0
        self.frameID = 0
        self.start_time = 0

        if(len(videofile)>0):
            self.cam = cv2.VideoCapture(videofile)
            self.playvideo = True
        else:
            self.cam = cv2.VideoCapture(0+id)
            #self.cam = cv2.VideoCapture(cv2.CAP_DSHOW+id)
            self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, size[0])
            self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, size[1])
            self.playvideo = False

    def working(self):
        webCam = self.cam
        if(webCam.isOpened() is True):
            return True
        else:
            if(self.playvideo is True):
                return True
            else:
                return False

    def camRealSize(self):
        webcam = self.cam
        width = int(webcam.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(webcam.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return (width, height)

    def getFrame(self, rotate=0, vflip=False, hflip=False, resize=None):
        webcam = self.cam
        hasFrame, frame = webcam.read()
        self.fps = webcam.get(cv2.CAP_PROP_FPS)
        if(frame is not None):
            frame = cv2.resize(frame, self.camsize)

            if(vflip==True):
                frame = cv2.flip(frame, 0)
            if(hflip==True):
                frame = cv2.flip(frame, 1)
    
            if(rotate>0):
                frame = imutils.rotate_bound(frame, rotate)
            if(resize is not None):
                frame = imutils.resize(frame, size=resize)

            if(self.frameID == 0):
                self.start_time = time.time()
            else:
                self.fps = self.frameID / (time.time() - self.start_time)

            self.frameID += 1

        else:
            hasFrame = False

        return hasFrame, frame

    def release(self):
        webcam = self.cam
        webcam.release()

class Desktop:
    def __init__(self, bg, winName, fullscreen=False):
        if(fullscreen is True):
            cv2.namedWindow(winName, cv2.WND_PROP_FULLSCREEN)        # Create a named window
            cv2.setWindowProperty(winName, cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        else:
            cv2.namedWindow(winName, cv2.WINDOW_NORMAL) 

        #cv2.setMouseCallback(winName, self.mouseClick)

        self.bg = cv2.imread(bg)
        self.winname = winName
        #self.btn_record = [ (cv2.imread("images/btn_record1.png"), (700,172)), (cv2.imread("images/btn_record2.png"), (700,172)), (cv2.imread("images/btn_record3.png"), (700,172)) ]
        #self.btn_detection = [ (cv2.imread("images/btn_detection2.png"), (700,262)), (cv2.imread("images/btn_detection.png"), (700,262)) ]
        #self.btn_poweroff = [ (cv2.imread("images/btn_poweroff2.png"), (700,373)), (cv2.imread("images/btn_poweroff.png"), (700,373)) ]
        self.xy = (0,0)
        self.action = None
        self.frame = (None, time.time())
        self.faceimg = None

    def display(self, frame=None, faceimg=None, frameSize=(430,323), frameXY=(28, 90)):
        bg2 = self.bg.copy()
        frame = cv2.resize(frame, frameSize) 
        y_point, x_point = frameXY[1], frameXY[0]
        frame_shape = frame.shape
        bg2[y_point:y_point+frame_shape[0], x_point:x_point+frame_shape[1]] = frame

        if(faceimg is not None):
            faceimg = cv2.resize(faceimg, (200,250))
            #print(faceimg.shape)
            #imgDetected = cv2.copyMakeBorder(detected[0], 6, 6, 6, 6, cv2.BORDER_CONSTANT, value=(255,255,255))
            bg2[45:45+faceimg.shape[0], 540:540+faceimg.shape[1]] = faceimg


        return bg2

    def getKeyin(self, x, y):
        bg = self.buttons
        keyin = None
        color = bg[y, x]
        b, g, r = color[0], color[1], color[2]
        if( b==1 and g==1 and r==1 ):
            keyin = "REC"
        elif( b==2 and g==2 and r==2 ):
            keyin = "OBJ"
        elif( b==3 and g==3 and r==3 ):
            keyin = "OFF"
        elif( b==4 and g==4 and r==4 ):
            keyin = "CHK"

        return keyin

    def mouseClick(self, event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.xy = (x,y)
            self.action = self.getKeyin(x, y)
            #print(self.action)
