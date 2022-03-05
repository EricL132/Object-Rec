import os
import pathlib
import tensorflow_hub as hub
import cv2
import numpy
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
import time
# Loading csv with labels of classes
labels = pd.read_csv(os.path.join(pathlib.Path(__file__).parent,'labels.csv'), sep=';', index_col='ID')
labels = labels['OBJECT (2017 REL.)']
detector = hub.load("https://tfhub.dev/tensorflow/efficientdet/lite2/detection/1")




def readImage(imageName):
    width = 1028
    height = 1028
    image_path = os.path.join(pathlib.Path(__file__).parent.parent.parent.parent,"tmp",imageName)
    img = cv2.imread(image_path)
    inp = cv2.resize(img, (width , height ))

    #Convert img to RGB
    rgb = cv2.cvtColor(inp, cv2.COLOR_BGR2RGB)

    # COnverting to uint8
    rgb_tensor = tf.convert_to_tensor(rgb, dtype=tf.uint8)

    #Add dims to rgb_tensor
    rgb_tensor = tf.expand_dims(rgb_tensor , 0)

    # Creating prediction
    boxes, scores, classes, num_detections = detector(rgb_tensor)

    # Processing outputs
    pred_labels = classes.numpy().astype('int')[0] 
    pred_labels = [labels[i] for i in pred_labels]
    pred_boxes = boxes.numpy()[0].astype('int')
    pred_scores = scores.numpy()[0]

    # Putting boxes and labels on the image
    for score, (ymin,xmin,ymax,xmax), label in zip(pred_scores, pred_boxes, pred_labels):
        if score < 0.5:
            continue
        img_boxes = cv2.rectangle(rgb,(xmin, ymax),(xmax, ymin),(0,255,0),2)      
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img_boxes, label,(xmin, ymax-10), font, 1.5, (255,0,0), 2, cv2.LINE_AA)
    plt.figure(figsize=(24,32))
    plt.axis('off')
    #save image to send back
    plt.imshow(img_boxes)
    plt.savefig(image_path,bbox_inches='tight', pad_inches = 0)

# import os
# import pathlib

# import matplotlib
# import matplotlib.pyplot as plt

# import io
# import scipy.misc
# import numpy as np
# from six import BytesIO
# from PIL import Image, ImageDraw, ImageFont
# from six.moves.urllib.request import urlopen
# from .readInfo import * 
# import tensorflow as tf
# import tensorflow_hub as hub

# from object_detection.utils import label_map_util
# from object_detection.utils import visualization_utils as viz_utils
# from object_detection.utils import ops as utils_ops



# PATH_TO_LABELS = './models/research/object_detection/data/mscoco_label_map.pbtxt'
# category_index = label_map_util.create_category_index_from_labelmap(os.path.join(pathlib.Path(__file__).parent.absolute(),PATH_TO_LABELS), use_display_name=True)


# print('loading model...')
# hub_model = hub.KerasLayer(os.path.join(pathlib.Path(__file__).parent.absolute(),"hub"))
# print('model loaded!')



# def getNewImage(imageName):
#     image_path = os.path.join(pathlib.Path(__file__).parent.parent.parent,"tmp",imageName)
    
#     image_np = load_image_into_numpy_array(image_path)
  
#     # running inference
#     results = hub_model(image_np)

#     # different object detection models have additional results
#     # all of them are explained in the documentation
#     result = {key:value.numpy() for key,value in results.items()}

#     label_id_offset = 0
#     image_np_with_detections = image_np.copy()

    
#     # Use keypoints if available in detections
#     keypoints, keypoint_scores = None, None
#     if 'detection_keypoints' in result:
#         keypoints = result['detection_keypoints'][0]
#         keypoint_scores = result['detection_keypoint_scores'][0]

#     viz_utils.visualize_boxes_and_labels_on_image_array(
#         image_np_with_detections[0],
#         result['detection_boxes'][0],
#         (result['detection_classes'][0] + label_id_offset).astype(int),
#         result['detection_scores'][0],
#         category_index,
#         use_normalized_coordinates=True,
#         max_boxes_to_draw=200,
#         min_score_thresh=.60,
#         agnostic_mode=False,
#         line_thickness=5,
#         keypoints=None,
#     )
#     plt.figure(figsize=(24,32))
#     plt.imshow(image_np_with_detections[0])
#     plt.axis('off')
#     plt.savefig(os.path.join(pathlib.Path(__file__).parent.parent.parent,"tmp",imageName),bbox_inches='tight', pad_inches = 0)


# """ import socketserver
# from http.server import BaseHTTPRequestHandler

# class MyHandler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         if self.path == '/captureImage':
#             getNewImage()
#         self.send_response(200)

# httpd = socketserver.TCPServer(("", 8080), MyHandler)
# httpd.serve_forever()
#  """
