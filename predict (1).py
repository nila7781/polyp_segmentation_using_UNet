# -*- coding: utf-8 -*-
"""predict.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16oHohfy5rtF-73tFdtEf6IR7JkOyhSYg
"""

import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.utils import CustomObjectScope
from tensorflow import keras
from tensorflow.keras import layers
from tqdm import tqdm
#from data import load_data, tf_dataset
#from train import iou

def read_image(path):
    x = cv2.imread(path, cv2.IMREAD_COLOR)
    x = cv2.resize(x, (224, 224))
    x = x/255.0
    return x

def read_mask(path):
    x = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    x = cv2.resize(x, (224, 224))
    x = np.expand_dims(x, axis=-1)
    return x
#for joining of image and predicted mask
def mask_parse(mask):
    mask = np.squeeze(mask)
    mask = [mask, mask, mask]
    mask = np.transpose(mask, (1, 2, 0))
    return mask


if __name__ == "__main__":
    ## Dataset
    path = "/content/drive/MyDrive/pp1/PROJECT/PROJECT/CVC-612/"
    batch_size = 16
    (train_x, train_y), (valid_x, valid_y), (test_x, test_y) = load_data(path)
    print(len(train_x), len(valid_x), len(test_x))
    test_dataset = tf_dataset(test_x, test_y, batch=batch_size)

    test_steps = len(test_x)//batch
    if len(test_x) % batch != 0:
        test_steps += 1
#loading the u net model
    with CustomObjectScope({'iou': iou}):
        model = tf.keras.models.load_model("/content/drive/MyDrive/pp1/PROJECT/PROJECT/files/model.h5")
#evaluateing the model
       # inputs=tf.Tensor(shape=(8,), dtype=str)
        #training=False
        #mask=None
        #model.evaluate(test_dataset , steps=test_steps)
    for i, (x, y) in tqdm(enumerate(zip(test_x, test_y)), total=len(test_x)):
        x = read_image(x)
        y = read_mask(y)
        y_pred = model.predict(np.expand_dims(x, axis=0))
        y_pred= y_pred[0]>0.5#if value of any pixel is gratern than 0.5 then it will work else it will be 0
        h, w, _ = x.shape
        white_line = np.ones((h, 10, 3)) * 255.0

        opt = tf.keras.optimizers.Adam(lr)
        metrics = ["acc", tf.keras.metrics.Recall(), tf.keras.metrics.Precision(), iou]
        model.compile(loss="binary_crossentropy", optimizer=opt, metrics=metrics)

        all_images = [
            x*255.0 , white_line,
            mask_parse(y), white_line,
            mask_parse(y_pred)*255.0
        ]
        image = np.concatenate(all_images, axis=1)
        cv2.imwrite(f"/content/drive/MyDrive/pp1/PROJECT/PROJECT/results/{i}.png", image)