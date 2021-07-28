import cv2
import numpy as np
from threading import Thread, Lock

from pytorchyolo import detect, models

class Detection:

    running = False
    lock = None

    model = None
    frame = None
    boxes = None


    def __init__(self):

        #self.model = models.load_model("PyTorch-YOLOv3/config/yolov3.cfg", "PyTorch-YOLOv3/yolov3.weights")
        self.model = models.load_model("PyTorch-YOLOv3/config/yolov3-tiny.cfg", "PyTorch-YOLOv3/yolov3-tiny.weights")

        self.lock = Lock()
        self.boxes = []
    

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
                boxes = detect.detect_image(self.model, self.frame)

                self.lock.acquire()
                self.boxes = boxes
                self.lock.release()

    # TODO: HSV Thresholding

    # TODO: detect uising matchTemplate

    # TODO: detect using cascade filters
