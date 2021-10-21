## Description

This computer vision aimbot provides character detection and targeting for video games that use humanoid character models. This aimbot approach is targeted at cloud hosted games as they are immune to tradisional cheats. Tradisional cheats require access to client side process memory, object code and network traffic. With cloud hosted games the user has no way to tamper with the internals of the game. 

This project is mainly a proof of concept as the computational requirements and level of performance renders this approach infeasible. 
For an overview of how this aimbot functions, see the [METHODOLOGY.md](https://github.com/RyanSawchuk/cv-aimbot/blob/main/METHODOLOGY.md) file.

### Built With

* [Python3](https://www.anaconda.com/products/individual)
* [YOLOv5](https://pytorch.org/hub/ultralytics_yolov5/)


## Getting Started

### Prerequisites

* [Python3](https://www.anaconda.com/products/individual)
* Cuda toolkit v11 if using an Nvidia GPU: 
```conda install pytorch torchvision torchaudio cudatoolkit=11.1 -c pytorch -c conda-forge```
  * [PyTorch Installation](https://pytorch.org/get-started/locally/)


### Installation

1. Clone the repo: 
   ```sh
   git clone https://github.com/RyanSawchuk/cv-aimbot.git
   ```
2. Install Python packages: 
   ```sh
   python -m pip install -r requirements.txt
   ```


## Usage

```python3
python aimbot.py
```


Exit key: ```'='```


Toggle firing key: ```'-'```

## Acknowledgments

* [YOLOv5](https://pytorch.org/hub/ultralytics_yolov5/)

