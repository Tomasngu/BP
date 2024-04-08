from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
from sklearn.model_selection import ParameterGrid
import os
# os.environ["CUDA_VISIBLE_DEVICES"] = "1"

#model = YOLO('yolov8l.pt').to('cuda:1')  # load an official model
#results = model.train(data='config.yaml', epochs=200, batch=16)

hyperparameter_grid = {
    # 'batch': [32, 64],      # Value (brightness) adjustment
    'batch': [16],      # Value (brightness) adjustment
}

parameter_grid = ParameterGrid(hyperparameter_grid)

for parameters in parameter_grid:
    # Set hyperparameters for the model
    model = YOLO('yolov8x.pt')  # load an official model
    print(parameters)
    results = model.train(data='config.yaml', epochs=300, **parameters, cache=True, device='0', verbose=False, project='large_run')
    