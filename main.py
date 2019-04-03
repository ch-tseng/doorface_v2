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
from libFace import PICam
from mtcnn.mtcnn import MTCNN

cameraType = 0  #0: PICamera. 1:Webcam

webcam_id = 0
webcam_size = (640, 480)
webcam_rotate = 0
webcam_flip_vertical = False
webcam_flip_horizontal = False

picam_size = (1296, 972)
picam_rotate = 180
picam_flip_vertical = False
picam_flip_horizontal = False

# Desktop
full_screen = False

interval_face_detect = 0.25  # seconds

#for debug
#simulate = "images/door_in_source.avi"
simulate = "resources/F_tea_area_200010_05.3gp"
#simulate = ""
write_video = False
video_file = "output/door_in_"+str(time.time())+".avi"

#-----------------------------------------------------------------------------
def init_env():
    '''
    if not os.path.exists(video_out):
        os.makedirs(video_out)

    if not os.path.exists(image_waiting_path):
        os.makedirs(image_waiting_path)

    if not os.path.exists(image_detected_path):
        os.makedirs(image_detected_path)

    '''
    if(full_screen is True):
        cv2.namedWindow(cv2_win_name, cv2.WND_PROP_FULLSCREEN)        # Create a named window
        cv2.setWindowProperty(cv2_win_name, cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

    print("init...")

def box_face(img, box, bcolor, bbold):
    x1, y1 = int(box[0]), int(box[1])
    x2, y2 = x1+int(box[2]), y1+int(box[3])

    cv2.rectangle(img, (x1, y1), (x2, y2), bcolor, bbold)
    facearea = img[y1:y2, x1:x2]

    return img, facearea

def putText(img, txt, loc, txtcolor, txtsize, txtbold):
    cv2.putText(img, str(txt), loc, cv2.FONT_HERSHEY_COMPLEX, txtsize, txtcolor, txtbold)
    return img

def detectFace(stopping):
    global DESKTOP
    #print("TEST: detectFace")
    while not stopping:

        frame_data = DESKTOP.frame
        img = frame_data[0]
        img_time = frame_data[1]

        if(img is not None):
            #print("TEST:", time.time() - img_time)
            if(time.time() - img_time < interval_face_detect):
                mtcnndata = detector.detect_faces(img)

                face_img = None
                #print(mtcnndata)
                if(len(mtcnndata)>0):
                    for facedata in mtcnndata:
                        img, face_img = box_face(img, facedata['box'], (0,255,0), 1)

                    DESKTOP.faceimg = face_img
                    #DESKTOP.img = img

#-----------------------------------------------------------------------------

bg_path = "images/desktop.png"
cv2_win_name = "face-desktop"

#-----------------------------------------------------------------------------
init_env()

stopping = []  #for threadding to run and stop
thread_facedetect = Thread(target=detectFace, args=(stopping,) )

detector = MTCNN()
DESKTOP = Desktop(bg_path, cv2_win_name, fullscreen=full_screen)

if(cameraType==1):
    CAMERA = webCam(id=webcam_id, videofile=simulate, size=webcam_size)
else:
    CAMERA = PICam(videofile="", size=picam_size, rotate=picam_rotate, vflip=False, hflip=False)

if(CAMERA.working() is False):
    print("webcam cannot work.")
    appStatus = False
    sys.exit()


if __name__ == '__main__':
    thread_facedetect.start()

    if(write_video is True):
        width = 800
        height = 480
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        out = cv2.VideoWriter(video_file, fourcc, 20.0, (int(width),int(height)))

    while True:

        if(cameraType==1):
            hasFrame, frame = CAMERA.getFrame(rotate=webcam_rotate, vflip=webcam_flip_vertical, hflip=webcam_flip_horizontal, resize=None)
        else:
            hasFrame, frame = CAMERA.getFrame()

        DESKTOP.frame = (frame.copy(), time.time())

        #print("CAM size:", frame.shape)
        if(hasFrame is False or frame is None):
            print("Cannot get image from webcam.")
            continue

        #mtcnndata = detector.detect_faces(frame)

        face_img = DESKTOP.faceimg
        #for facedata in mtcnndata:
        #    frame, face_img = box_face(frame, facedata['box'], (0,255,0), 3)

        img = DESKTOP.display(frame=frame, faceimg=face_img, frameSize=(430,323), frameXY=(30, 107))
        #img = putText(img, 'FPS:'+str(round(CAMERA.fps,2)), (360, 140), (0,255,0), 1.0, 2)
        #cv2.imwrite("demo/demo_"+str(time.time())+".jpg", img)

        cv2.imshow(cv2_win_name, img)
        if(write_video is True):
            out.write(img)

        #outDemo.write(img_desktop)
        cv2.waitKey(1)

        print("FPS:", CAMERA.fps)
