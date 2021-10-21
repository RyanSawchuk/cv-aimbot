import cv2

class Vision:

    def __init__(self):
        pass
    
    def draw_crosshair(self, frame, target):
        # TODO: drawmarker()
        cv2.circle(frame, target, 15, (60,150,230), 2)
        cv2.circle(frame, target, 3, (60,150,230), 2)
        return frame

    def get_priority_target(self, boxes):
        max_bb_area = 0
        target = None

        for box in boxes:
            if box[5] == 0:
                xB = int(box[2])
                xA = int(box[0])
                yB = int(box[3])
                yA = int(box[1])

                if (xB - xA) * (yB - yA) > max_bb_area:
                    max_bb_area = (xB - xA) * (yB - yA)
                    target = self.head_circle_center(xA, yA, xB, yB, 0.1)
        return target

    def draw_bounding_boxes(self, frame, boxes):
        for box in boxes:
            if box[5] == 0:
                xB = int(box[2])
                xA = int(box[0])
                yB = int(box[3])
                yA = int(box[1])

                cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
                cv2.circle(frame, self.head_circle_center(xA, yA, xB, yB, 0.1), self.head_circle_radius(xA, yA, xB, yB), (0, 0, 255), 2)
                cv2.putText(frame, f"{box[4]: .2f}", (xA,yA-10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
        return frame

    def head_circle_radius(self, xA, yA, xB, yB):
        return int(((yB - yA) * (xB - xA)) ** (1/3.5))

    def head_circle_center(self, xA, yA, xB, yB, offset):
        return (int((xA + xB)/2), int(yA - (offset * (yA - yB))))
