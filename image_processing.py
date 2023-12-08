from typing import (
    Optional,
    Tuple,
    Generator,
    Union,
    Dict,
    Any,
)
from pathlib import Path
import contextlib
import os
import sys

from tqdm.auto import trange, tqdm
import matplotlib.pyplot as plt
import numpy as np
import cv2

os.environ["OPENCV_FFMPEG_LOGLEVEL"]="-8"

PX_INTENSITY_THRESHOLD: int = 100
GLOBAL_THRESHOLD: int = 10**6


def open_video(path: Union[str,os.PathLike]) -> Tuple[cv2.VideoCapture, int]:
    cap = cv2.VideoCapture(str(path))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    return cap, frame_count

def get_frame(cap: cv2.VideoCapture, n: int) -> Optional[cv2.Mat]:
    cap.set(cv2.CAP_PROP_POS_FRAMES, n)
    ret, frame = cap.read()
    return frame if ret is not None else None

def get_frame_rate(cap: cv2.VideoCapture) -> Optional[int]:
    return cap.get(cv2.CAP_PROP_FPS)

def draw_bbox(frame: cv2.Mat, bbox: Dict) -> Tuple[cv2.Mat,cv2.Mat]:
    x,y,w,h = bbox["x"],bbox["y"],bbox["w"],bbox["h"]
    rect = frame[y:y+h,x:x+w].copy()
    return cv2.rectangle(frame.copy(),(x,y),(x+w,y+h),(255,255,0),2), rect
