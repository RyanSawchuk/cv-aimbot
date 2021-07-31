import numpy as np
import cv2
from threading import Thread, Lock

from mss import mss
from PIL import Image
from time import time

class GameCapture:

    running = False
    lock = None

    screen_capture = None
    capture_area = None
    frame = None
    capture_frame = None
    frame_number = 0
    

    def __init__(self, w, h):
        self.lock = Lock()
        self.screen_capture = mss()
        self.capture_area = {"left": 0, "top": 0, "width": w, "height": h}
        self.capture_frame = self.capture_frame_by_PIL

    
    def start(self):
        self.running = True
        t = Thread(target=self.run)
        t.start()


    def stop(self):
        self.running = False


    def run(self):
        self.frame_number = 0
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


    # TODO: Read frames from capture card