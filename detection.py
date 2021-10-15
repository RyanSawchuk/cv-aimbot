import cv2
import numpy as np
from threading import Thread, Lock
from time import time

import torch

class Detection:

    running = False
    lock = None

    model = None
    frame = None
    predictions = None
    tracker = None

    def __init__(self):
        device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True, verbose=False).to(device)

        # TODO: fix version conflicts
        #self.tracker = cv2.legacy.MultiTracker_create()
        self.lock = Lock()
        self.predictions = []
    

    def get_model_device(self):
        return next(self.model.parameters()).device.type


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
                predictions = self.detect(self.frame)

                self.lock.acquire()
                self.predictions = predictions
                self.lock.release()


    def detect(self, frame):
        return self.model(frame).pred[0].tolist()


    # TODO: refactor returned box format
    def track_objects(self, frame):

        max_objects = 16
        success = False
        predictions = None
        
        if len(self.tracker.getObjects()) == 0 or success is False:
            predictions = self.detect.detect_image(self.model, frame)

        for i, box in enumerate(predictions):
            if i == max_objects:
                break

            # Filter out non human detections
            if int(box[5]) != 0:
                continue

            bbox = (box[0], box[1], box[2], box[3])
            self.tracker.add(cv2.legacy.TrackerKCF_create(), frame, bbox)
    
        else:
            success, predictions = self.tracker.update(frame)
        
        return predictions
