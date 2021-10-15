import warnings
warnings.filterwarnings("ignore")

import os, sys
import numpy as np

import pyautogui
import keyboard as kb
import cv2
import argparse
import re

from time import time, sleep
from threading import Thread, Lock

from gamecapture import GameCapture
from detection import Detection
from vision import Vision
from utilities import Utilities

import win32gui

pyautogui.PAUSE = 0


class AimBot:

    is_running = False
    is_active = False
    lock = None
    state = None

    frame = None
    active_targets = None
    action_history = None
    start_time = 0


    def __init__(self):
        self.lock = Lock()
        self.active_targets = []
        self.action_history = []
        self.start_time = time()

    
    def shoot(self, target):
        # TODO: PyDirectInput for DirectX on windows
        # TODO: Check that the target is within screen bounds
        try:
            pyautogui.moveTo(target[0], target[1])
            pyautogui.click()
            self.action_history.append((time() - self.start_time, target))

        except pyautogui.FailSafeException as e:
            pyautogui.moveTo(0, 0)
            #pyautogui.click()
            self.action_history.append((time() - self.start_time, (0, 0)))
    

    def start(self):
        self.is_running = True
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.lock.acquire()
        self.is_running = False
        self.lock.release()
    
    def update(self, frame):
        self.lock.acquire()
        self.frame = frame
        self.lock.release()

    def toggle(self):
        self.lock.acquire()
        self.is_active = not self.is_active
        self.lock.release()

    def is_active(self):
        active = 0
        self.lock.acquire()
        active = self.is_active
        self.lock.release()
        return active

    def run(self):
        while self.running:
            # TODO: shoot active target
            pass


def main():

    sw = pyautogui.size()[0]
    sh = pyautogui.size()[1]

    mr = 3
    
    wn = 'Play - Stadia - Google Chrome'
    wn = 'Main Monitor'
    #multi_thread(sw, sh, wn)

    single_thread(sw, sh, mr, wn)


# TODO: add this funtionality tot he aimbot class
def single_thread(sw, sh, mirror_scale, windowname):

    capture = GameCapture(sw, sh, windowname, 'WIN32GUI')
    detector = Detection()
    vision = Vision()
    aimbot = AimBot()

    # TODO: fix
    args["record"] = 'live_capture'
    args['togglekey'] = '~'

    mask = np.zeros(sw, dtype=bool)
    mask[range(520, 2400+520)] = True

    record = type(args['record']) == str
    if record:
        num = len([re.match(f'^{args["record"]}', f) for f in os.listdir("output")])
        fps = Utilities.fps_test2(sw, sh)
        print(f'FPS: {fps}')
        out = cv2.VideoWriter(f'output/{args["record"]}-{num}.mp4', cv2.VideoWriter_fourcc(*'mp4v'), int(fps), (sw, sh))
    
    start_time = time()
    frames = 0

    running = True
    while running:
        frames += 1
        try:

            if kb.is_pressed(args['togglekey']):
                aimbot.is_active = not aimbot.is_active
            if kb.is_pressed('='):
                running = False
                aimbot.is_active = False
                continue
            
            frame = capture.capture_frame()
            #frame = frame[:,mask]

            if aimbot.is_active:
                predictions = detector.detect(frame)

                target = vision.get_priority_target(predictions)
                frame = vision.draw_bounding_boxes(frame, predictions)
                frame = vision.draw_crosshair(frame, target)

                if target is not None:
                    #aimbot.shoot(target)
                    pass

            if record:
                out.write(frame)
            
            cv2.imshow('MIRROR: ' + windowname, cv2.resize(frame, (0,0), fx=1/mirror_scale, fy=1/mirror_scale))
            if cv2.waitKey(25) & 0xFF == ord('='):
                running = False
        
        except Exception as e:
            print(e)
            
    run_time = time() - start_time
    print(f'FPS: {frames / (run_time)}')

    if record:
        out.release()
    cv2.destroyAllWindows()

    with open('output/actions.txt', 'w') as f:
        for action in aimbot.action_history:
            f.write(str(action))


# TODO: fix
def multi_thread(sw, sh, windowname):

    capture = GameCapture(sw, sh)
    detector = Detection()
    vision = Vision()
    aimbot = AimBot()

    record = type(args['record']) == str
    if record:
        num = len([re.match(f'^{args["record"]}', f) for f in os.listdir("output")])
        fps = Utilities.fps_test(sw, sh)
        out = cv2.VideoWriter(f'output/{args["record"]}-{num}.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (sw*2, sh*2))
    
    capture.start()
    detector.start()
    aimbot.start()

    while True:
        try:
            if capture.frame is None:
                continue
            
            detector.update(capture.frame)

            # TODO: align bounding predictions with the correct frame OR reduce detect time by x10
            target = vision.get_priority_target(detector.predictions)
            frame = vision.draw_bounding_boxes(detector.frame, detector.predictions)
            frame = vision.draw_crosshair(frame, target)

            if target is not None:
                aimbot.shoot(target)

            if record:
                out.write(frame)
        
        except Exception as e:
            print(e)
            pass
    
    capture.stop()
    detector.stop()
    aimbot.stop()

    if record:
        out.release()

    with open('output/actions.txt', 'w') as f:
        for action in aimbot.action_history:
            f.write(str(action))
    pass


parser = argparse.ArgumentParser()
parser.add_argument('--record', metavar='<output video file name>', type=str, default=False, help='Record the live capture to an mp4 file.')
parser.add_argument('--togglekey', metavar='<key bind>', type=str, default=False, help='Set the key bind for toggling the aimbot.')
args = vars(parser.parse_args())


if __name__ == '__main__':
    main()