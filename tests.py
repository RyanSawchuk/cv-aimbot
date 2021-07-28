import warnings
warnings.filterwarnings("ignore")

import os, sys
import cv2
import numpy as np
import time
import pyautogui

from pytorchyolo import detect, models

import aimbot


def main():
    #single_frame()
    mouse_positioning()
    pass


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