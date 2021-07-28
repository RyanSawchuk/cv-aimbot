import warnings
warnings.filterwarnings("ignore")

import os, sys

import pyautogui

from time import time, sleep
from threading import Thread, Lock

from gamecapture import GameCapture
from detection import Detection
from vision import Vision
from utilities import Utilities

pyautogui.PAUSE = 0


class AimBot:

    running = False
    lock = None
    state = None

    active_targets = None
    frame = None
    action_history = None


    def __init__(self):
        self.lock = Lock()
        self.active_targets = []
        self.action_history = []

    
    def target_player(self):
        pass
    

    def start(self):
        self.running = True
        t = Thread(target=self.run)
        t.start()


    def stop(self):
        self.running = False
    
    
    def update(self, frame):
        self.lock.acquire()
        self.frame = frame
        self.lock.release()


    def run(self):
        while self.running:
            pass


def usage():
    print(f'Usage: ')
    sys.exit(0)


def main():

    sw = pyautogui.size()[0]
    sh = pyautogui.size()[1]
    
    capture = GameCapture(sw, sh)
    detector = Detection()
    vision = Vision()
    aimbot = AimBot()

    capture.start()
    detector.start()

    rtime = 0
    epoch = 0

    while True:
        
        start = time()

        if capture.frame is None:
            continue
        
        detector.update(capture.frame)

        frame = vision.draw_bounding_boxes(detector.frame, detector.boxes)
        frame = vision.draw_crosshair(frame, vision.get_priority_target(detector.boxes))

        # TODO: bot actions

        rtime += time() - start
        epoch += 1

        if rtime > 1 * 10:
            break
    
    capture.stop()
    detector.stop()
    print(f'FPS: {1 / (rtime / epoch)}')

if __name__ == '__main__':
    main()