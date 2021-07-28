import cv2
import numpy as np

class Utilities:

    def __init__(self):
        pass
    
    # TODO: fix
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


@staticmethod
def check_fps(input_video):
    cap = cv2.VideoCapture(input_video)
    print(f'FPS: {cap.get(cv2.CAP_PROP_FPS)}')
    cap.release()