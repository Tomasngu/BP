import numpy as np
import cv2
from object_detection.builders import model_builder
from object_detection.utils import visualization_utils as viz_utils
from object_detection.utils import config_util
from object_detection.utils import label_map_util
import tensorflow as tf
import os
import json
import six
import collections
import math
import tqdm
import argparse


PATH_TO_LABELS = os.path.join('inference_graph', 'labelmap.pbtxt')
PATH_TO_CONFIG = os.path.join('inference_graph', 'pipeline.config')
CATEGORY_INDEX = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS,
                                                                    use_display_name=True)
OUTPUT_JSON = 'a.json'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'    # Suppress TensorFlow logging
tf.get_logger().setLevel('ERROR')
INPUT_DIR = '../captured_frames'


@tf.function
def detect_fn(image, detection_model):
    """Detect objects in image."""

    image, shapes = detection_model.preprocess(image)
    prediction_dict = detection_model.predict(image, shapes)
    detections = detection_model.postprocess(prediction_dict, shapes)

    return detections, prediction_dict, tf.reshape(shapes, [-1])


category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS,
                                                                    use_display_name=True)


def predict_elephants(image_path, detection_model):
    image_np = cv2.imread(image_path)
    input_tensor = tf.convert_to_tensor(
        np.expand_dims(image_np, 0), dtype=tf.float32)
    detections, predictions_dict, shapes = detect_fn(
        input_tensor, detection_model)
    label_id_offset = 1
    image_np_with_detections = image_np.copy()

    min_score_thresh = 0.40

    box_to_display_str_map = collections.defaultdict(list)
    box_to_color_map = collections.defaultdict(str)

    number_of_items = 0

    for i in range(detections['detection_boxes'][0].numpy().shape[0]):

        if detections['detection_scores'][0].numpy() is None or detections['detection_scores'][0].numpy()[i] > min_score_thresh:

            box = tuple(detections['detection_boxes'][0].numpy()[i].tolist())

            display_str = ''

            if (detections['detection_classes'][0].numpy() + label_id_offset).astype(int)[i] in six.viewkeys(category_index):
                class_name = category_index[(detections['detection_classes'][0].numpy(
                ) + label_id_offset).astype(int)[i]]['name']
                display_str = str(class_name)
                display_str = '{}: {}%'.format(display_str, round(
                    100*detections['detection_scores'][0].numpy()[i]))

                box_to_display_str_map[box].append(display_str)

                box_to_color_map[box] = "Red"

                if "Elephant" in box_to_display_str_map[box][0]:
                    number_of_items += 1
    im_width, im_height = image_np.shape[1::-1]

    for box, color in box_to_color_map.items():
        ymin, xmin, ymax, xmax = box

        ymin = ymin * im_height
        xmin = xmin * im_width
        ymax = ymax * im_height
        xmax = xmax * im_width

        x = xmin
        y = ymin
        w = xmax - xmin
        h = ymax - ymin

        box_color = (0, 0, 0)

        if color == "Red":
            box_color = (0, 0, 255)

        cv2.rectangle(image_np_with_detections, (int(x), int(y)),
                      (int(x) + int(w), int(y) + int(h)), box_color, 4)
        cv2.putText(image_np_with_detections, 'Elephant', (int(x), int(
            y)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    return image_np_with_detections, number_of_items, detections


def get_image_metadata(image_path, cnt, dataset_id=1):
    image_metadata = {}
    image_np = cv2.imread(image_path)
    height, width, _ = image_np.shape
    image_metadata['id'] = cnt
    image_metadata['dataset_id'] = dataset_id
    image_metadata['path'] = image_path
    image_metadata['height'], image_metadata['width'] = height, width
    image_metadata['file_name'] = os.path.basename(image_path)
    return image_metadata


def convert_to_coco(tf_detections, images_metadata):
    coco_output = {
        "images": [],
        "categories": [
            {"id": 1, "name": "Elephant", "supercategory": "", "color": "#3ab7dd", "metadata": {}, "keypoint_colors": []}
        ],
        "annotations": []
    }
    annotation_id = 1
    for image_metadata, detection in zip(images_metadata, tf_detections):
        # Add image info
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

        # Process each detection
        for box, score, class_id in zip(detection['detection_boxes'][0], detection['detection_scores'][0], detection['detection_classes'][0]):
            if score < 0.4: 
                continue

            # Convert TensorFlow box format to COCO format
            ymin, xmin, ymax, xmax = box.numpy()
            xmin = xmin * image_metadata["width"]
            ymin = ymin * image_metadata["height"]
            xmax = xmax * image_metadata["width"]
            ymax = ymax * image_metadata["height"]
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

    return coco_output

def main(input_dir):
    configs = config_util.get_configs_from_pipeline_file(PATH_TO_CONFIG)
    model_config = configs['model']
    detection_model = model_builder.build(
        model_config=model_config, is_training=False)

    images_metadata = []
    tf_detections = []

    for i, filename in enumerate(tqdm.tqdm(os.listdir(input_dir))):
        image_path = os.path.join(input_dir, filename)
        _, _,  detections = predict_elephants(image_path, detection_model)
        tf_detections.append(detections)
        metadata = get_image_metadata(image_path, i+1)
        images_metadata.append(metadata)
    coco_dataset = convert_to_coco(tf_detections, images_metadata)
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(coco_dataset, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get annotations from your data.')
    parser.add_argument("--dir", default=INPUT_DIR, help="Input your image directory.")
    args = parser.parse_args()
    main(args.dir)
