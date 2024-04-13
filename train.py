from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
from sklearn.model_selection import ParameterGrid
from detector.elephant_detector import ElephantDetector
import os
# os.environ["CUDA_VISIBLE_DEVICES"] = "1"


hyperparameter_grid = {
    'lr0': [0.001, 0.01],       
    'batch': [16, 32],     
    'optimizer':['SGD', 'AdamW']
}

parameter_grid = ParameterGrid(hyperparameter_grid)

for parameters in parameter_grid:
    detector = ElephantDetector()
    detector.train(**parameters)
    
    