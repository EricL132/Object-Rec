import os
import pathlib

import matplotlib
import matplotlib.pyplot as plt

import io
import scipy.misc
import numpy as np
from six import BytesIO
from PIL import Image, ImageDraw, ImageFont
from six.moves.urllib.request import urlopen
from .readInfo import * 
import tensorflow as tf
import tensorflow_hub as hub

from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.utils import ops as utils_ops



PATH_TO_LABELS = './models/research/object_detection/data/mscoco_label_map.pbtxt'
category_index = label_map_util.create_category_index_from_labelmap(os.path.join(pathlib.Path(__file__).parent.absolute(),PATH_TO_LABELS), use_display_name=True)


print('loading model...')
hub_model = hub.KerasLayer(os.path.join(pathlib.Path(__file__).parent.absolute(),"hub"))
print('model loaded!')



def getNewImage(imageName):
    image_path = os.path.join(pathlib.Path(__file__).parent.parent.parent,"tmp",imageName)
    
    image_np = load_image_into_numpy_array(image_path)
  
    # running inference
    results = hub_model(image_np)

    # different object detection models have additional results
    # all of them are explained in the documentation
    result = {key:value.numpy() for key,value in results.items()}

    label_id_offset = 0
    image_np_with_detections = image_np.copy()

    
    # Use keypoints if available in detections
    keypoints, keypoint_scores = None, None
    if 'detection_keypoints' in result:
        keypoints = result['detection_keypoints'][0]
        keypoint_scores = result['detection_keypoint_scores'][0]

    viz_utils.visualize_boxes_and_labels_on_image_array(
        image_np_with_detections[0],
        result['detection_boxes'][0],
        (result['detection_classes'][0] + label_id_offset).astype(int),
        result['detection_scores'][0],
        category_index,
        use_normalized_coordinates=True,
        max_boxes_to_draw=200,
        min_score_thresh=.60,
        agnostic_mode=False,
        line_thickness=5,
        keypoints=None,
    )
    plt.figure(figsize=(24,32))
    plt.imshow(image_np_with_detections[0])
    plt.axis('off')
    plt.savefig(os.path.join(pathlib.Path(__file__).parent.parent.parent,"tmp",imageName),bbox_inches='tight', pad_inches = 0)


""" import socketserver
from http.server import BaseHTTPRequestHandler

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/captureImage':
            # Insert your code here
            getNewImage()

        self.send_response(200)

httpd = socketserver.TCPServer(("", 8080), MyHandler)
httpd.serve_forever()
 """