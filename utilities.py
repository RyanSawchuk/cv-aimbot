import cv2
import numpy as np

from time import time, sleep

from gamecapture import GameCapture
from detection import Detection
from vision import Vision

class Utilities:

    def __init__(self):
        pass
    

    @staticmethod
    def check_fps(input_video):
        cap = cv2.VideoCapture(input_video)
        print(f'FPS: {cap.get(cv2.CAP_PROP_FPS)}')
        cap.release()


    # Multi thread
    # TODO: Refactor
    @staticmethod
    def fps_test(w, h):
        # C: 162, 0.08039550722381215
        # D: 13, 0.774630069732666

        cap = GameCapture(w, h)
        
        cap.start()
        sleep(3)
        cap.stop()
        
        print(f'FPS: {int(cap.frame_number / 3)}')

        return int(cap.frame_number / 3)


    # Single thread
    def fps_test2(sw, sh):
        capture = GameCapture(sw, sh)
        detector = Detection()
        vision = Vision()

        rtime = 0

        for _ in range(12):
            start = time()

            frame = capture.capture_frame_by_PIL()

            boxes = detector.detect_YOLOv3(frame)

            target = vision.get_priority_target(boxes)
            frame = vision.draw_bounding_boxes(frame, boxes)
            frame = vision.draw_crosshair(frame, target)

            rtime += time() - start

        return int(12 / rtime)


    # TODO: refactor
    @staticmethod
    def process_video(filename):

        cap = cv2.VideoCapture(filename)
        out = cv2.VideoWriter(f'output/{sys.argv[2]}', cv2.VideoWriter_fourcc(*'mp4v'), int(cap.get(cv2.CAP_PROP_FPS)), (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

        model = models.load_model("PyTorch-YOLOv3/config/yolov3.cfg", "PyTorch-YOLOv3/yolov3.weights")
        #model = models.load_model("PyTorch-YOLOv3/config/yolov3-tiny.cfg", "PyTorch-YOLOv3/yolov3-tiny.weights")

        while cap.isOpened():
            ret, frame = cap.read()
            
            if not ret:
                break

            frame, target = process_frame(model, frame)
            out.write(frame)

        out.release()
        cap.release()

    # TODO: refactor
    @staticmethod
    def alter_fps(input_video, output_video, scale):

        cap = cv2.VideoCapture(input_video)
        out = cv2.VideoWriter(f'{output_video}', cv2.VideoWriter_fourcc(*'mp4v'), int(cap.get(cv2.CAP_PROP_FPS) / scale), (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

        counter = 0

        while cap.isOpened():
            ret, frame = cap.read()
            
            if not ret:
                break
            
            if counter % scale == 0:
                out.write(frame)

            counter += 1

        out.release()
        cap.release()