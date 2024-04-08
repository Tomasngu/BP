from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
from sklearn.model_selection import ParameterGrid
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1"

#model = YOLO('yolov8l.pt').to('cuda:1')  # load an official model
#results = model.train(data='config.yaml', epochs=200, batch=16)

hyperparameter_grid = {
    'lr0': [0.001, 0.01],         # Initial learning rate            # Final learning rate as a factor of lr0
    'batch': [16, 32],      # Value (brightness) adjustment
    'optimizer':['SGD', 'AdamW']
}

parameter_grid = ParameterGrid(hyperparameter_grid)

for parameters in parameter_grid:
    # Set hyperparameters for the model
    model = YOLO('yolov8l.pt')  # load an official model
    print(parameters)
    results = model.train(data='config.yaml', epochs=300, **parameters, cache=False, device='1', verbose=False, project='best_run')
    