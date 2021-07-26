import warnings
warnings.filterwarnings("ignore")

import os, sys

import numpy as np
import cv2
import time
import pyautogui
import time
from PIL import Image

from pytorchyolo import detect, models


def usage():
    print(f'Usage: ')
    sys.exit(0)


def main():

    #process_video(sys.argv[1])

    capture_screen(5)
    

def capture_screen(fps):

    #model = models.load_model("PyTorch-YOLOv3/config/yolov3.cfg", "PyTorch-YOLOv3/yolov3.weights")
    model = models.load_model("PyTorch-YOLOv3/config/yolov3-tiny.cfg", "PyTorch-YOLOv3/yolov3-tiny.weights")

    # pyautogui havles screen res on mac m1
    sw = pyautogui.size()[0] * 2
    sh = pyautogui.size()[1] * 2

    out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (sw, sh))

    sc = mss()
    rect = {"left": 0, "top": 0, "width": sw/2, "height": sh/2}

    while True:
        start = time.time()
        
        frame = sc.grab(rect)
        frame = np.asarray(Image.frombytes("RGB", frame.size, frame.bgra, "raw", "BGRX"))#.transpose(1,0,2)
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame = process_frame(model, frame)

        print(time.time() - start)

        # update mouse positißn

        out.write(frame)
        
    out.release()


def process_frame(model, frame):

    scale = 1
    #_frame = preprocess_frame(frame, scale)
    _frame = cv2.resize(frame, (int(frame.shape[1] / scale), int(frame.shape[0] / scale)), interpolation = cv2.INTER_AREA)

    boxes = detect.detect_image(model, _frame)

    for box in boxes:
        if box[5] == 0:
            xB = int(box[2]) * scale
            xA = int(box[0]) * scale
            yB = int(box[3]) * scale
            yA = int(box[1]) * scale
            cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
            cv2.circle(frame, head_circle_center(xA, yA, xB, yB, 0.1), head_circle_radius(xA, yA, xB, yB), (0, 0, 255), 2)
            cv2.putText(frame, f"{box[4]: .2f}", (xA,yA-10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

    return frame


def head_circle_radius(xA, yA, xB, yB):
    return int(((yB - yA) * (xB - xA)) ** (1/3.5))


def head_circle_center(xA, yA, xB, yB, offset):
    return (int((xA + xB)/2), int(yA - (offset * (yA - yB))))


def preprocess_frame(frame, scale):

    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.resize(frame, (int(frame.shape[1] / scale), int(frame.shape[0] / scale)), interpolation = cv2.INTER_AREA)

    return frame


def process_video(filename):

    cap = cv2.VideoCapture(filename)
    out = cv2.VideoWriter(f'output/{sys.argv[2]}.mp4', cv2.VideoWriter_fourcc(*'mp4v'), int(cap.get(cv2.CAP_PROP_FPS)), (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

    model = models.load_model("PyTorch-YOLOv3/config/yolov3.cfg", "PyTorch-YOLOv3/yolov3.weights")
    #model = models.load_model("PyTorch-YOLOv3/config/yolov3-tiny.cfg", "PyTorch-YOLOv3/yolov3-tiny.weights")

    while cap.isOpened():
        ret, frame = cap.read()
        
        if not ret:
            break

        frame = process_frame(model, frame)
        out.write(frame)

    out.release()
    cap.release()


# Requires opencv-contrib-python and a virtual env
def filter(model, tracker, frame):

    scale = 3
    max_objects = 16

    # Gray Scale and Resize
    _frame = frame
    #_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _frame = cv2.resize(_frame, (int(_frame.shape[1] / scale), int(_frame.shape[0] / scale)), interpolation = cv2.INTER_AREA)

    boxes = None
    success = False

    # Image segmentation and object detection
    if len(tracker.getObjects()) == 0 or success is False:
        boxes = detect.detect_image(model, _frame)

        for i, box in enumerate(boxes):
            # Prevent tracking more than 16 objects (or specified max)
            if i == max_objects:
                break

            # Filter out non human detections
            if int(box[5]) != 0:
                continue

            bbox = (box[0], box[1], box[2], box[3])
            tracker.add(cv2.legacy.TrackerKCF_create(), _frame, bbox)
    
    else:
        success, boxes = tracker.update(_frame)

    # Draw bounding boxes, head circles and entity number
    for i, box in enumerate(boxes):
        xB = int(box[2]) * scale
        xA = int(box[0]) * scale
        yB = int(box[3]) * scale
        yA = int(box[1]) * scale
        cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
        cv2.circle(frame, head_circle_center(xA, yA, xB, yB, 0.1), head_circle_radius(xA, yA, xB, yB), (0, 0, 255), 2)
        #cv2.putText(frame, f"{box[4]: .2f}", (xA,yA-10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
        cv2.putText(frame, f"Entity: {i+1}", (xA,yA-10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

    return frame


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


def check_fps(input_video):
    cap = cv2.VideoCapture(input_video)
    print(f'FPS: {cap.get(cv2.CAP_PROP_FPS)}')
    cap.release()


if __name__ == '__main__':
    main()