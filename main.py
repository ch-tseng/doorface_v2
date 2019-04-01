#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import random
from threading import Thread
import signal, sys, os, glob
import time, datetime
import cv2
import numpy as np
import imutils
from libFace import webCam
from libFace import Desktop

webcam_id = 0
webcam_size = (640, 480)
webcam_rotate = 0
webcam_flip_vertical = False
webcam_flip_horizontal = False

picam_rotate = 0
picam_flip_vertical = False
picam_flip_horizontal = False

# Desktop
full_screen = True

#for debug
simulate = ""

#-----------------------------------------------------------------------------
def init_env():
    '''
    if not os.path.exists(video_out):
        os.makedirs(video_out)

    if not os.path.exists(image_waiting_path):
        os.makedirs(image_waiting_path)

    if not os.path.exists(image_detected_path):
        os.makedirs(image_detected_path)

    if(full_screen is True):
        cv2.namedWindow(cv2_win_name, cv2.WND_PROP_FULLSCREEN)        # Create a named window
        cv2.setWindowProperty(cv2_win_name, cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    '''

    print("init...")
#-----------------------------------------------------------------------------

bg_path = "images/desktop.png"
cv2_win_name = "face-desktop"

if __name__ == '__main__':
    init_env()

    DESKTOP = Desktop(bg_path, cv2_win_name, fullscreen=full_screen)

    CAMERA = webCam(id=webcam_id, videofile=simulate, size=webcam_size)
    if(CAMERA.working() is False):
        print("webcam cannot work.")
        appStatus = False
        sys.exit()

    frameID = 0

    while True:
        hasFrame, frame = CAMERA.getFrame(rotate=webcam_rotate, vflip=webcam_flip_vertical, hflip=webcam_flip_horizontal, resize=None)
        #print("CAM size:", frame.shape)
        if(hasFrame is False or frame is None):
            print("Cannot get image from webcam.")

        img = DESKTOP.display(frame=frame, frameSize=(430,323), frameXY=(30, 107))
        cv2.imshow(cv2_win_name, img)
        #outDemo.write(img_desktop)
        cv2.waitKey(1)
