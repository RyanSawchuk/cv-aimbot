import warnings
warnings.filterwarnings("ignore")

import os, sys
import cv2
import numpy as np
import pandas as pd
import time
import pyautogui

import win32gui
import win32api
import torch

from threading import Thread, Lock

from gamecapture import GameCapture
from detection import Detection
from vision import Vision
from utilities import Utilities

def main():
    sw = pyautogui.size()[0] #win32api.GetSystemMetrics(0)
    sh = pyautogui.size()[1] #win32api.GetSystemMetrics(0)

    #Utilities.fps_test(sw, sh, 'Play - Stadia - Google Chrome')
    Utilities.process_video('hitman3_dubia.mp4')

    #record_window('Play - Stadia - Google Chrome', 'out')
    #single_frame_yolov5()
    pass


def record_window(windowname, filename):

    sw = pyautogui.size()[0] #win32api.GetSystemMetrics(0)
    sh = pyautogui.size()[1] #win32api.GetSystemMetrics(0)

    print(sw, sh)

    cap = GameCapture(sw, sh, windowname, 'WIN32GUI')
    win32gui.SetForegroundWindow( win32gui.FindWindow(None, windowname))

    path = f"output\\{filename}.mp4"
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    
    #fps = Utilities.fps_test(sw, sh, 'Play - Stadia - Google Chrome')
    fps = 52
    writer = cv2.VideoWriter(path, fourcc, fps, (sw, sh))


    start = time.time()
    for _ in range(1800):

        frame = cap.capture_frame()

        writer.write(frame)
    
    writer.release()
    print(f'FPS: {1800/(time.time() - start)}')


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


def single_frame_yolov5():

    sw = pyautogui.size()[0] #win32api.GetSystemMetrics(0)
    sh = pyautogui.size()[1] #win32api.GetSystemMetrics(0)

    cap = GameCapture(sw, sh, 'Play - Stadia - Google Chrome', 'WIN32GUI')
    vision = Vision()
    time.sleep(3)

    start = time.time()

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(device)

    #frame = cap.capture_frame()
    frame = cv2.imread('data/warlock_fit2.png')
    print(frame.shape)

    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True).to(device)

    results = model(frame)

    print(f'Time: {time.time() - start}')
    print(results.pred[0].tolist())

    target = vision.get_priority_target(results.pred[0].tolist())
    frame = vision.draw_bounding_boxes(frame, results.pred[0].tolist())
    frame = vision.draw_crosshair(frame, target)

    cv2.imwrite('output/single_frame_y5.png', frame)


if __name__ == '__main__':
    main()