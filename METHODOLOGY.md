# Computer Vision Aimbot

## Project Motivation
The primary motivation for this project is a proof of concept to demonstrate that a computer vision approach for an aimbot is possible for cloud hosted games. The secondary motivation for this project is to exercise my programming skills in a computer vision context. 


## Functional Overview

### Screen Capturing
- A single thread captures the active screen by taking a screenshot in a loop using the [win32api](https://github.com/mhammond/pywin32) for Windows or the [mss](https://github.com/BoboTiG/python-mss) screen capture library for MacOS or Linux. 


### Detection

![Character Model Detection](images/example.png "Character Model Detection")

![Character Model Detection and Tracking](images/test2.gif "Character Model Detection and Tracking")

This bot uses the [YOLOv5](https://pytorch.org/hub/ultralytics_yolov5/) object detection model to detect humanoid figures in captured frames. This network was trained using real world photographs of various scenes containing many different types of objects, including humans. This model can be used to detect humanoid character models in video game screen captures. However this model does not functional perfectly in the context of Destiny 2 and will miss some characters. In practice, any object detection model trained on photographs of humans should work in a video game context that uses humanoid character models.


### Tracking
The [Lucas–Kanade method](https://en.wikipedia.org/wiki/Lucas–Kanade_method) is used to track detected objects between frames. This method is only used when capturing frames at a rate that is `>= 60` fps. The Lucas-Kanade method is ineffective when the frames are captured at a rate `< 60` fps because the change in position of objects between frames will be to large to track effectively. If the captured frame rate is `< 60` fps objects will be redetected in each frame instead. 


### Enemy Prioritization

![Target Prioritization](images/example2.png "Target Prioritization")

The priority target is the character model who's bounding box has the largest area. The bounding box area is a proxy for how close the character is to yourself. Character models with large bounding box areas tend to be close while character models with small bounding box areas tend to be far away. In comparison with tradisional aimbots, the distance between your character and every opposing character is calculated given the (x, y, z) coordinates of each character entity. The closest visible character is selected as the target.



### Enemy Targeting and Automated Mouse Input

- direct x

## Comparison To Tradisional Aimbot
Temp


## Pitfalls 
### Full and Partial Occlusion
- Enemies behind cover (partial)
- Enemies peek shooting (partial or full)
- inability to detect enemies that arent on the screen (full)

### False positives and False Negatives
- Team mates are indistinguishable from enemies (false positive)
- Non character models detected (false positive)
- Missed character models (false negative)


## Hardware and Computational Requirements


### GPU
Temp

### FPS
- `>= 30`


## Potential Improvements and Future Work
Temp


## References
1. Temp