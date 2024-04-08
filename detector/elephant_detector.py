from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
import torch
import os
import tqdm
import json
import shutil

class ElephantDetector:
    """A class for detecting elephants in images using a YOLO model."""

    def __init__(self, model_path=None):
        """
        Initializes the ElephantDetector.

        Parameters:
        - model_path (str, optional): Path to the YOLO model weights file. If None, defaults to 'yolov8l.pt'.
        """
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f'device = {self.device}')
        if model_path is None:
            self.model = YOLO('yolov8l.pt').to(self.device)
        else:
            self.model = YOLO(model_path).to(self.device)
            
    def predict_img(self, image_path, conf=0.5):
        """
        Predicts elephants in a single image.

        Parameters:
        - image_path (str): Path to the image file.
        - conf (float, optional): Confidence threshold for detections.
        """
        if not os.path.isfile(image_path):
            raise Exception('Path is not a file')
        return self.model(source=image_path, conf=conf, stream=False)
    
    def predict_dir(self, dir_path, conf=0.5):
        """
        Predicts elephants in all images within a directory.

        Parameters:
        - dir_path (str): Path to the directory containing images.
        - conf (float, optional): Confidence threshold for detections.
        """
        if not os.path.isdir(dir_path):
            raise Exception('Path not found or is not a directory')
        return self.model(source=dir_path, conf=conf, stream=True)

    @staticmethod
    def get_image_metadata(result, cnt, dataset_id=1):
        """
        Generates metadata for an image based on the detection result.

        Parameters:
        - result: Detection result object for the image.
        - cnt (int): Unique identifier for the image.
        - dataset_id (int, optional): Identifier for the dataset the image belongs to.
        """
        image_metadata = {}
        height, width = result.orig_shape
        image_metadata['id'] = cnt
        image_metadata['dataset_id'] = dataset_id
        image_metadata['path'] = result.path
        image_metadata['height'], image_metadata['width'] = height, width
        image_metadata['file_name'] = os.path.basename(result.path)
        return image_metadata

    def add_coco(self, coco_output, image_metadata, result, annotation_id):
        """
        Adds COCO-format annotations for detected elephants to the output.

        Parameters:
        - coco_output (dict): The COCO output dictionary to append annotations to.
        - image_metadata (dict): Metadata for the image being annotated.
        - result: Detection result object for the image.
        - annotation_id (int): Unique identifier for the annotation.
        """
        coco_output["images"].append({
            "id": image_metadata["id"],
            "dataset_id": image_metadata["dataset_id"],
            "category_ids": [],
            "path": os.path.join('datasets', image_metadata["path"]),
            "width": image_metadata["width"],
            "height": image_metadata["height"],
            "file_name": image_metadata["file_name"],
            "annotated": False,
            "annotating": [],
            "num_annotations": 0,
            "metadata": {},
            "deleted": False,
            "milliseconds": 0,
            "events": [],
            "regenerate_thumbnail": False
        })
        for x in result.boxes:
            xmin, ymin, xmax, ymax = x.cpu().numpy().xyxy[0]
            xmin, ymin, xmax, ymax = xmin.item(), ymin.item(), xmax.item(), ymax.item()
            ymin, xmin, ymax, xmax = round(ymin, 1), round(xmin, 1), round(ymax, 1), round(xmax, 1)
            x, y, w, h = xmin, ymin, (xmax - xmin), (ymax - ymin)
            x, y, w, h = round(x, 1), round(y, 1), round(w, 1), round(h, 1)
            segmentation_points = [xmin, ymin, xmax, ymin, xmax, ymax, xmin, ymax]
            coco_output["annotations"].append({
                "id": annotation_id,
                "image_id": image_metadata["id"],
                "category_id": 1,
                "segmentation": [segmentation_points], 
                "area": round(w * h, 0),
                "bbox": [x, y, w, h],
                "iscrowd": False,
                "isbbox": True,
                "color": "#8eb517", 
                "metadata": {}
            })
            annotation_id += 1
        return annotation_id

    def remove_empty(self, dir_path, split_path='SLONI_empty'):
        """
        Moves images with no detected elephants to a separate directory.

        Parameters:
        - dir_path (str): Path to the directory containing images.
        - split_path (str, optional): Path to the directory where images with no detections will be moved.
        """
        os.makedirs(split_path, exist_ok=True)
        for filename in tqdm.tqdm(os.listdir(dir_path)):
            file_path = os.path.join(dir_path, filename)
            results = self.predict_img(file_path, conf=0.4)
            if len(results.boxes) == 0:
                shutil.move(file_path, os.path.join(split_path, filename))
            
        
    def yolo_annotate(self, dir_path, output_path='output_labels'):
        """
        Saves YOLO format annotations for detected elephants in images.

        Parameters:
        - dir_path (str): Path to the directory containing images to annotate.
        - output_path (str, optional): Path to save the annotations.
        """

        tmp_dir = 'tmp_outs'
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
        if os.path.exists(output_path):
            shutil.rmtree(output_path)
        self.model(dir_path, conf=0.5, save_txt=True, project=tmp_dir, device=self.device)
        shutil.move(os.path.join(tmp_dir, 'predict'), output_path)
        shutil.rmtree(tmp_dir)

    def coco_annotate(self, dir_path, output_path='labels.json'):
        """
        Saves COCO format annotations for detected elephants in images.

        Parameters:
        - dir_path (str): Path to the directory containing images to annotate.
        - output_path (str, optional): Path to save the annotations in COCO format.
        """
        results = self.predict_dir(dir_path)
        coco_output = {
            "images": [],
            "categories": [
                {"id": 1, "name": "Elephant", "supercategory": "", "color": "#3ab7dd", "metadata": {}, "keypoint_colors": []}
            ],
            "annotations": []
        }
        annotation_id = 1
        for i, result in enumerate(results, 1):
            image_metadata = self.get_image_metadata(result, i)
            annotation_id = self.add_coco(coco_output, image_metadata, result, annotation_id)
        print(coco_output)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(coco_output, f, ensure_ascii=False, indent=4)
    
        
    def show(self, img):
        """
        Displays an image.

        Parameters:
        - img: The image to display.
        """
        plt.figure()
        plt.axis('off')
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)) 
        plt.show()
    def show_labeled(self, img_path, show=True):
        """
        Displays an image with labeled detections.

        Parameters:
        - img_path (str): Path to the image file.
        - show (bool, optional): Whether to show labels and probabilities on the image.
        """
        result = self.predict_img(img_path)
        if not show:
            labeled_img = result[0].plot(labels=False, probs=False)
        else:
            labeled_img = result[0].plot()
        self.show(labeled_img)
        
    def train(self, data='config.yaml', epochs=300, project='train_run', **parameters):
        results = self.model.train(data=data, epochs=epochs, cache=False, device=self.device, verbose=False, project=project, **parameters)
        return results
        