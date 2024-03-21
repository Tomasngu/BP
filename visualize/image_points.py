import numpy as np
import cv2

ELEPHANT_SIZE = 2.5
IMG_WIDTH, IMG_HEIGHT = 1920, 1000

MAP_WIDTH_12, MAP_HEIGHT_12 = 846, 572
MAP_REAL_WIDTH_12 = 12

MAP_WIDTH_6, MAP_HEIGHT_6 = 890, 573
MAP_REAL_WIDTH_6 = 60

MAP_WIDTH_4, MAP_HEIGHT_4 = 730, 488
MAP_REAL_WIDTH_4 = 45

MAP_WIDTH_7, MAP_HEIGHT_7 = 608, 572
MAP_REAL_WIDTH_7 = 9

IMAGE_PTS_1 = np.array([[342, 272], [1346, 120], [1320, 396], [598, 410]])
MAP_PTS_1 = np.array([[169, 555],  [20, 243], [281, 292], [282, 458]])
H1, _ = cv2.findHomography(IMAGE_PTS_1, MAP_PTS_1)

IMAGE_PTS_2 = np.array([[35, 447], [1050, 299], [912, 405], [281, 513]])
MAP_PTS_2 = np.array([[685, 242],  [678, 552], [599, 463], [599, 291]])
H2, _ = cv2.findHomography(IMAGE_PTS_2, MAP_PTS_2)

IMAGE_PTS_4 = np.array([[748, 340],[1711, 375], [1778, 148],[1044, 91],  [430, 55],[175, 151]])
MAP_PTS_4 = np.array([ [456, 411], [619, 411], [700, 174], [470, 170], [147, 43], [43, 128]])
H4, _ = cv2.findHomography(IMAGE_PTS_4, MAP_PTS_4)

IMAGE_PTS_6 = np.array([[1394, 416], [1158, 326], [248, 428], [600, 342]])
MAP_PTS_6 = np.array([[563, 62], [360, 32], [363, 391], [95, 263]])
H6, _ = cv2.findHomography(IMAGE_PTS_6, MAP_PTS_6)

IMAGE_PTS_7 = np.array([[711, 544],[1353, 564], [1651, 402],[633, 187]])
MAP_PTS_7 = np.array([ [347, 331], [348, 462], [444, 556], [598, 286]])
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

def shift(x, y, width, height, camera):
    if camera in [1, 2, 4, 6, 7]:
        y += height/3
    else:
        y += height/2
    return x, y, width, height