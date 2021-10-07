# Destiny 2 Computer Vision Aimbot POC

## Project Motivation
Cloud gaming platforms such as Stadia are popular alternatives to PC for competitive PVP gamemodes because cloud hosted games are immune to tradisional cheats. Tradisional cheats require access to client side process memory, code and network traffic. With cloud hosted games the user has no way to tamper with the internals of the game. 

The primary motivation for this project is a proof of concept to demonstrate that a computer vision approach for an aimbot is possible for cloud hosted games. The secondary motivation for this project is to exercise my programming skills in a computer vision context. 


## Disclaimer
I have no intent on productionizing and distributing this aimbot. I have no intent of using this aimbot in actual game play as the the computational requirements and performance level will be impractical. 


## Functional Overview

## Screen Capturing
The screen is captured using a loop that repeatedly takes a screen shot of the active screen. This approach is capable of recording the screen at `<= 30` fps when the screen capture component is running on it's own thread. A better approach I plan on implementing uses the Windows GUI API to read frames directly from the game window. The Windows GUI API approach can capture frames at a rate of `~30` fps when the screen capture component is running on it's own thread. Furthermore, I intend on using a capture card to directly record frames at `>= 60` fps. The capture card approach is by far the most effective but has very demanding hardware and computational requirements. 


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

## Hardware and Computational Requirements

### Capture Card
Temp

### GPU
Temp

### FPS
- `>= 60`



## Comparison To Tradisional Aimbot
Temp


## Potential Improvements and Future Work
Temp


## References
1. Temp
