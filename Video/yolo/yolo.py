#  @Project SmartAlarm
#  @Copyright (c) 2019 AIPower. All Rights Reserved.

import os

import numpy as np
import tensorflow as tf
from keras import backend as kb
from keras.models import load_model
from PIL import Image

from .yolo3.model import yolo_eval
from .yolo3.utils import letterbox_image

from config import log


class YOLO:
    def __init__(self):
        self.model_name = 'yolo.h5'
        self.model_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'model_data',
            self.model_name,
        )
        self.anchors_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'model_data',
            'yolo_anchors.txt',
        )
        self.classes_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'model_data',
            'coco_classes.txt',
        )
        self.score = 0.5
        self.iou = 0.5
        self.class_names = self._get_class()
        self.anchors = self._get_anchors()
        self.graph = tf.compat.v1.get_default_graph()  # work with tensorflow 1.15.0 not 2.0.0
        self.sess = kb.get_session()
        self.model_image_size = (416, 416)  # fixed size or (None, None)
        self.is_fixed_size = self.model_image_size != (None, None)

        self.yolo_model = load_model(self.model_path, compile=False)
        log.info(f"Loaded model {self.model_name} successfully!")

        self.input_image_shape = kb.placeholder(shape=(2,))

        self.boxes, self.scores, self.classes = yolo_eval(
            self.yolo_model.output, self.anchors,
            len(self.class_names), self.input_image_shape,
            score_threshold=self.score, iou_threshold=self.iou
        )

    def _get_class(self):
        with open(self.classes_path) as f:
            class_names = f.readlines()
        class_names = [c.strip() for c in class_names]
        return class_names

    def _get_anchors(self):
        with open(self.anchors_path) as f:
            anchors = f.readline()
            anchors = [float(x) for x in anchors.split(',')]
            anchors = np.array(anchors).reshape(-1, 2)
        return anchors

    def detect_image(self, image: Image):

        if self.is_fixed_size:
            boxed_image = letterbox_image(image, tuple(reversed(self.model_image_size)))
        else:
            new_image_size = (
                image.width - (image.width % 32),
                image.height - (image.height % 32)
            )
            boxed_image = letterbox_image(image, new_image_size)

        image_data = np.array(boxed_image, dtype='float32')

        image_data /= 255.
        image_data = np.expand_dims(image_data, 0)  # Add batch dimension.

        with self.graph.as_default():
            out_boxes, out_scores, out_classes = self.sess.run(
                [self.boxes, self.scores, self.classes],
                feed_dict={
                    self.yolo_model.input: image_data,
                    self.input_image_shape: [image.size[1], image.size[0]],
                    kb.learning_phase(): 0
                })

        return_boxs = []
        for i, c in reversed(list(enumerate(out_classes))):
            predicted_class = self.class_names[c]
            if predicted_class != 'person':
                continue
            if out_scores[i] < self.score:
                continue
            box = out_boxes[i]
            left = int(box[1])
            top = int(box[0])
            right = int(box[3])
            bottom = int(box[2])
            return_boxs.append(
                (left, top, right, bottom)
            )

        return return_boxs

    def close_session(self):
        self.sess.close()
