import numpy as np
import cv2

ELEPHANT_SIZE = 2

IMG_WIDTH, IMG_HEIGHT = 1920, 1000 
MAP_WIDTH_12, MAP_HEIGHT_12 = 856, 572
MAP_REAL_WIDTH_12 = 20


IMAGE_PTS_1 = np.array([[342, 272], [1346, 120], [1320, 396], [598, 410]])
MAP_PTS_1 = np.array([[179, 555],  [30, 243], [291, 292], [292, 458]])
H1, _ = cv2.findHomography(IMAGE_PTS_1, MAP_PTS_1)


IMAGE_PTS_2 = np.array([[35, 447], [1050, 299], [912, 405], [281, 513]])
MAP_PTS_2 = np.array([[695, 242],  [688, 552], [609, 463], [609, 291]])
H2, _ = cv2.findHomography(IMAGE_PTS_2, MAP_PTS_2)

IMAGE_PTS_6 = np.array([[35, 447], [1050, 299], [912, 405], [281, 513]])
MAP_PTS_6 = np.array([[695, 242],  [688, 552], [609, 463], [609, 291]])
H6, _ = cv2.findHomography(IMAGE_PTS_6, MAP_PTS_6)

CAMERA_to_H = {
    1: H1,
    2: H2,
    6: H6
}

CAMERA_to_MAP = {
    1: (MAP_WIDTH_12, MAP_HEIGHT_12),
    2: (MAP_WIDTH_12, MAP_HEIGHT_12),
}
OPPOSING_CAMERA= {
    1: 2,
    2: 1,
}
CAMERA_to_REAL = {
    1: MAP_REAL_WIDTH_12,
    2: MAP_REAL_WIDTH_12
}