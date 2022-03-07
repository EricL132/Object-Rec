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
# detector = hub.KerasLayer(os.path.join(pathlib.Path(__file__).parent.absolute(),"hub"))




def readImage(filepath):
    width = 1300
    height = 700

    img = cv2.imread(filepath)
    inp = cv2.resize(img, (width , height ))

    #Convert img to RGB
    rgb = cv2.cvtColor(inp, cv2.COLOR_BGR2RGB)

    #Converting to uint8
    rgb_tensor = tf.convert_to_tensor(rgb, dtype=tf.uint8)

    #Add dims to rgb_tensor
    rgb_tensor = tf.expand_dims(rgb_tensor , 0)

    #Prediction results
    boxes, scores, classes, num_detections = detector(rgb_tensor)

    #Outputs from detection
    pred_labels = classes.numpy().astype('int')[0] 
    pred_labels = [labels[i] for i in pred_labels]
    pred_boxes = boxes.numpy()[0].astype('int')
    pred_scores = scores.numpy()[0]

    for score, (ymin,xmin,ymax,xmax), label in zip(pred_scores, pred_boxes, pred_labels):
        if score < 0.5:
            continue
        #Draw boxes
        img_boxes = cv2.rectangle(rgb,(xmin, ymax),(xmax, ymin),(0,255,0),2)     
        #Text settings 
        cv2.putText(img_boxes, label,(xmin, ymax-10), cv2.FONT_HERSHEY_DUPLEX , .5, (255,0,0), 1, cv2.LINE_AA)
    plt.figure(figsize=(32,24),dpi=96)
    plt.axis('off')
    #Save image
    plt.imshow(img_boxes)
    plt.savefig(filepath,bbox_inches='tight', pad_inches = 0)