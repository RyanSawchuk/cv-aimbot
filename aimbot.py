import warnings
warnings.filterwarnings("ignore")

import os, sys

import pyautogui
import cv2

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
    start_time = 0


    def __init__(self):
        self.lock = Lock()
        self.active_targets = []
        self.action_history = []
        self.start_time = time()

    
    def shoot(self, target):
        # TODO: PyDirectInput for DirectX on windows
        pyautogui.moveTo(target[0], target[1])
        pyautogui.click()
        self.action_history.append((time() - self.start_time, target))
    

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
            # TODO: shoot active target
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
    aimbot.start()

    rtime = 0
    epoch = 0

    record = True

    if record:
        fps = 23 #15 - 30
        out = cv2.VideoWriter('output/live_output1.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (sw*2, sh*2))

    while True:
        
        start = time()

        if capture.frame is None:
            continue
        
        detector.update(capture.frame)

        # TODO: align bounding boxes with the correct frame OR reduce detect time by x10
        target = vision.get_priority_target(detector.boxes)
        frame = vision.draw_bounding_boxes(detector.frame, detector.boxes)
        frame = vision.draw_crosshair(frame, target)

        # TODO: bot actions
        #aimbot.shoot(target)

        if record:
            out.write(frame)

        rtime += time() - start
        epoch += 1

        if rtime > 1 * 10:
            break
    
    capture.stop()
    detector.stop()
    aimbot.stop()

    out.release()

    print(f'FPS: {1 / (rtime / epoch)}')


if __name__ == '__main__':
    main()