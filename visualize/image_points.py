import numpy as np
import cv2
import os

ELEPHANT_SIZE = 2.5
IMG_WIDTH, IMG_HEIGHT = 1920, 1000

MAP_WIDTH_12, MAP_HEIGHT_12 = 686, 470
MAP_REAL_WIDTH_12 = 20

MAP_WIDTH_6, MAP_HEIGHT_6 = 890, 573
MAP_REAL_WIDTH_6 = 68

MAP_WIDTH_4, MAP_HEIGHT_4 = 730, 488
MAP_REAL_WIDTH_4 = 51

MAP_WIDTH_7, MAP_HEIGHT_7 = 610, 470
MAP_REAL_WIDTH_7 = 18

IMAGE_PTS_1 = np.array([[342, 272], [1346, 120], [1320, 396], [598, 410]])
MAP_PTS_1 = np.array([[162, 464],  [12, 153], [272, 202], [272, 370]])
H1, _ = cv2.findHomography(IMAGE_PTS_1, MAP_PTS_1)

IMAGE_PTS_2 = np.array([[35, 447], [1050, 299], [912, 405], [281, 513]])
MAP_PTS_2 = np.array([[678, 153],  [673, 463], [592, 372], [592, 200]])
H2, _ = cv2.findHomography(IMAGE_PTS_2, MAP_PTS_2)

IMAGE_PTS_4 = np.array([[748, 340],[1711, 375], [1778, 148],[1044, 91],  [430, 55],[175, 151]])
MAP_PTS_4 = np.array([ [456, 411], [619, 411], [700, 174], [470, 170], [147, 43], [43, 128]])
H4, _ = cv2.findHomography(IMAGE_PTS_4, MAP_PTS_4)

IMAGE_PTS_6 = np.array([[1394, 416], [1158, 326], [248, 428], [600, 342]])
MAP_PTS_6 = np.array([[563, 62], [360, 32], [363, 391], [95, 263]])
H6, _ = cv2.findHomography(IMAGE_PTS_6, MAP_PTS_6)

IMAGE_PTS_7 = np.array([[711, 544],[1353, 564], [1651, 402],[633, 187]])
MAP_PTS_7 = np.array([ [347, 241], [347, 369], [444, 464], [598, 192]])
H7, _ = cv2.findHomography(IMAGE_PTS_7, MAP_PTS_7)

CAMERA_to_H = {
    1: H1,
    2: H2,
    4: H4,
    6: H6,
    7: H7
}

CAMERA_to_MAP = {
    1: (MAP_WIDTH_12, MAP_HEIGHT_12),
    2: (MAP_WIDTH_12, MAP_HEIGHT_12),
    4: (MAP_WIDTH_4, MAP_HEIGHT_4),
    6: (MAP_WIDTH_6, MAP_HEIGHT_6),
    7: (MAP_WIDTH_7, MAP_HEIGHT_7)
}

CAMERA_to_REAL = {
    1: MAP_REAL_WIDTH_12,
    2: MAP_REAL_WIDTH_12,
    4: MAP_REAL_WIDTH_4,
    6: MAP_REAL_WIDTH_6,
    7: MAP_REAL_WIDTH_7
}

MODULE_DIR = os.path.dirname(__file__)
CAMERA_to_PATH = {
    1: os.path.join(MODULE_DIR, 'maps/map12.png'),
    2: os.path.join(MODULE_DIR, 'maps/map12.png'),
    4: os.path.join(MODULE_DIR, 'maps/map4_real.png'),
    6: os.path.join(MODULE_DIR, 'maps/map6_real.png'),
    7: os.path.join(MODULE_DIR, 'maps/map7.png')
}

CAMERA_to_BACKGROUND = {
    1: os.path.join(MODULE_DIR, 'backgrounds/background1.png'),
    2: os.path.join(MODULE_DIR, 'backgrounds/background2.png'),
    4: os.path.join(MODULE_DIR, 'backgrounds/background4.png'),
    6: os.path.join(MODULE_DIR, 'backgrounds/background6.png'),
    7: os.path.join(MODULE_DIR, 'backgrounds/background7.png'),
}

def shift(x, y, width, height, camera):
    y += height/3
    return x, y, width, height