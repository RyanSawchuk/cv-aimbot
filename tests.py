import warnings
warnings.filterwarnings("ignore")

import os, sys
import cv2
import numpy as np
import time
import pyautogui

#from pytorchyolo import detect, models

from threading import Thread, Lock

from gamecapture import GameCapture
#from detection import Detection
from vision import Vision
from utilities import Utilities


def main():
    #single_frame()
    #mouse_positioning()
    hsv_tool()
    pass


def hsv_tool():

    from hsvfilter import HsvFilter, HsvPannel

    pannel = HsvPannel()

    pannel.init_control_gui()

    hsv_filter = HsvFilter(0, 180, 129, 15, 229, 243, 143, 0, 67, 0)
    
    sw = pyautogui.size()[0]
    sh = pyautogui.size()[1]
    cap = GameCapture(sw/2, sh/2)

    while True:
        frame = cap.capture_frame_by_PIL()

        hsv_filter = pannel.get_hsv_filter_from_controls()

        frame = pannel.apply_hsv_filter(frame, hsv_filter)

        cv2.imshow('Processed', frame)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break



def check_recording_fps():
    pass

def mouse_positioning():
    time.sleep(3)
    pyautogui.moveTo(120, 120)
    time.sleep(1)
    pyautogui.moveTo(500, 500)
    time.sleep(1)
    pyautogui.moveTo(900, 500)


def single_frame():
    model = models.load_model("PyTorch-YOLOv3/config/yolov3.cfg", "PyTorch-YOLOv3/yolov3.weights")
    #model = models.load_model("PyTorch-YOLOv3/config/yolov3-tiny.cfg", "PyTorch-YOLOv3/yolov3-tiny.weights")

    frame = cv2.imread(sys.argv[1])

    start = time.time()

    frame, target = aimbot.process_frame(model, frame)

    cv2.imwrite(str(sys.argv[2]), frame)

    cv2.imshow('frame', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()