import warnings
warnings.filterwarnings("ignore")

import os, sys

import pyautogui
import cv2
import argparse
import re

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
        try:
            pyautogui.moveTo(target[0], target[1])
            pyautogui.click()
            self.action_history.append((time() - self.start_time, target))

        except pyautogui.FailSafeException as e:
            pyautogui.moveTo(0, 0)
            #pyautogui.click()
            self.action_history.append((time() - self.start_time, (0, 0)))
    

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


def main():

    sw = pyautogui.size()[0]
    sh = pyautogui.size()[1]
    
    #multi_thread(sw, sh)

    single_thread(sw, sh)


def single_thread(sw, sh):

    capture = GameCapture(sw, sh)
    detector = Detection()
    vision = Vision()
    aimbot = AimBot()

    record = type(args['record']) == str
    if record:
        num = len([re.match(f'^{args["record"]}', f) for f in os.listdir("output")])
        fps = Utilities.fps_test2(sw, sh)
        print(f'FPS: {fps}')
        out = cv2.VideoWriter(f'output/{args["record"]}-{num}.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (sw*2, sh*2))
    
    try:
        while True:
            frame = capture.capture_frame_by_PIL()

            boxes = detector.detect_YOLOv3(frame)

            target = vision.get_priority_target(boxes)
            frame = vision.draw_bounding_boxes(frame, boxes)
            frame = vision.draw_crosshair(frame, target)

            if target is not None:
                aimbot.shoot(target)

            if record:
                out.write(frame)

    except Exception as e:
        #print(e)
        pass

    if record:
        out.release()

    with open('output/actions.txt', 'w') as f:
        for action in aimbot.action_history:
            f.write(str(action))


def multi_thread(sw, sh):

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

    try:
        while True:
            
            if capture.frame is None:
                continue
            
            detector.update(capture.frame)

            # TODO: align bounding boxes with the correct frame OR reduce detect time by x10
            target = vision.get_priority_target(detector.boxes)
            frame = vision.draw_bounding_boxes(detector.frame, detector.boxes)
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
args = vars(parser.parse_args())


if __name__ == '__main__':
    main()