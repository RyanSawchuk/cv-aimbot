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

    pass


def check_recording_fps():
    pass


def single_frame_test():
    #model = models.load_model("PyTorch-YOLOv3/config/yolov3.cfg", "PyTorch-YOLOv3/yolov3.weights")
    model = models.load_model("PyTorch-YOLOv3/config/yolov3-tiny.cfg", "PyTorch-YOLOv3/yolov3-tiny.weights")

    frame = cv2.imread(sys.argv[1])
    print(frame.shape)

    start = time.time()

    frame = aimbot.process_frame(model, frame)

    print(time.time() - start)

    cv2.imshow('frame', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()