import cv2
import numpy as np
from threading import Thread, Lock
from time import time

#from pytorchyolo import detect, models

class Detection:

    running = False
    lock = None

    model = None
    frame = None
    boxes = None
    detect_func = None
    tracker = None

    def __init__(self):

        #self.model = models.load_model("PyTorch-YOLOv3/config/yolov3.cfg", "PyTorch-YOLOv3/yolov3.weights")
        self.model = models.load_model("PyTorch-YOLOv3/config/yolov3-tiny.cfg", "PyTorch-YOLOv3/yolov3-tiny.weights")
        # TODO: fix version conflicts
        #self.tracker = cv2.legacy.MultiTracker_create()
        self.lock = Lock()
        self.boxes = []
        self.detect_func = self.detect_YOLOv3
    

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
            if self.frame is not None:
                boxes = self.detect_func(self.frame)

                self.lock.acquire()
                self.boxes = boxes
                self.lock.release()


    # TODO: refactor to use precompiled opencv implementation
    def detect_YOLOv3(self, frame):
        return detect.detect_image(self.model, frame)


    # TODO: refactor returned box format
    def track_objects(self, frame):

        max_objects = 16
        success = False
        boxes = None
        
        if len(self.tracker.getObjects()) == 0 or success is False:
            boxes = self.detect.detect_image(self.model, frame)

        for i, box in enumerate(boxes):
            if i == max_objects:
                break

            # Filter out non human detections
            if int(box[5]) != 0:
                continue

            bbox = (box[0], box[1], box[2], box[3])
            self.tracker.add(cv2.legacy.TrackerKCF_create(), frame, bbox)
    
        else:
            success, boxes = self.tracker.update(frame)
        
        return boxes


    # TODO: HSV Thresholding

    # TODO: detect using matchTemplate

    # TODO: detect using cascade filters
