import numpy as np
import cv2
from threading import Thread, Lock

from mss import mss
from PIL import Image
from time import time

import win32gui
import win32ui
import win32con


class GameCapture:

    running = False
    lock = None

    screen_capture = None
    capture_area = None
    frame = None
    capture_frame = None
    windowname = None
    frame_number = 0
    w = 0
    h = 0
    

    def __init__(self, w, h, windowname = '', method = 'PIL'):
        self.lock = Lock()
        self.screen_capture = mss()
        self.capture_area = {"left": 0, "top": 0, "width": w, "height": h}
        self.w = w
        self.h = h
        self.windowname = windowname

        if method == 'PIL':
            self.capture_frame = self.capture_frame_by_PIL
        elif method == 'WIN32GUI':
            self.capture_frame = self.capture_frame_by_WIN32
        else:
            self.capture_frame = self.capture_frame_by_PIL

    
    def start(self):
        self.running = True
        t = Thread(target=self.run)
        t.start()


    def stop(self):
        self.running = False


    def run(self):
        self.frame_number = 0

        if not self.windowname:
            win32gui.SetForegroundWindow(self.windowname)
        
        while self.running:
            frame = self.capture_frame()

            self.lock.acquire()
            self.frame = frame
            self.frame_number += 1
            self.lock.release()

    
    # TODO: Refactor
    def capture_frame_by_PIL(self):
        frame = self.screen_capture.grab(self.capture_area)
        frame = np.asarray(Image.frombytes("RGB", frame.size, frame.bgra, "raw", "BGRX"))#.transpose(1,0,2)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame


    # TODO: Capture frames using Quartz


    # TODO: Capture frames using win32gui
    def capture_frame_by_WIN32(self):

        #hwnd = win32gui.FindWindow(None, self.windowname)
        hwnd = win32gui.GetDesktopWindow()
        wDC = win32gui.GetWindowDC(hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)

        cDC = dcObj.CreateCompatibleDC()
        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(bmp)
        cDC.BitBlt((0,0), (self.w, self.h), dcObj, (0,0), win32con.SRCCOPY)
        
        signedIntsArray = bmp.GetBitmapBits(True)
        frame = np.fromstring(signedIntsArray, dtype='uint8')
        frame.shape = (self.h, self.w, 4)

        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, wDC)
        win32gui.DeleteObject(bmp.GetHandle())

        return cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)


    # TODO: Read frames from capture card