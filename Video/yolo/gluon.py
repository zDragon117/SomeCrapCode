#  @Project SmartAlarm
#  @Copyright (c) 2019 AIPower. All Rights Reserved.
from datetime import datetime
import mxnet as mx
from gluoncv import model_zoo, data
import cv2
import os
import numpy as np


class GLUON:
    def __init__(self):
        try:
            self.is_have_gpus = mx.context.num_gpus() > 0
            self.ctx = mx.gpu(0) if self.is_have_gpus else mx.cpu(0)
            self.net = model_zoo.get_model('yolo3_darknet53_coco', pretrained=True, ctx=self.ctx)
            # self.net = model_zoo.get_model('yolo3_darknet53_coco', pretrained=True)
            self.score = 0.5
            self.net.reset_class(classes=['person'], reuse_weights=['person'])
        except Exception as exc:
            print(exc)

        # in case encounter error "cudaMalloc failed: out of memory" (the reason maybe gpus memory size is not enough)
        # for now, the temporary solution is comment this line
        # self.net.hybridize()

    def detect_image(self, image):
        return_boxs = []
        # current_time = datetime.now().strftime("%H:%M:%S:%f")
        # print(current_time, image.shape)
        # cv2.imwrite('images/'+current_time, image)
        # print(mx.context.gpu_memory_info(0))
        img = mx.nd.array(image)
        # calculate scale ratio
        h, w, _ = img.shape
        scale_ratio = 416 / h if h < w else 416 / w

        x, img = data.transforms.presets.yolo.transform_test(img)

        # Error: Parameter 'darknetv30_conv0_weight' was not initialized on context cpu(0). It was only initialized on [gpu(0)].
        # Solution: https://github.com/dmlc/gluon-cv/issues/420
        if self.is_have_gpus:
            class_IDs, scores, bounding_boxs = self.net(x.as_in_context(mx.gpu(0)))
        else:
            class_IDs, scores, bounding_boxs = self.net(x)

        # class_IDs, scores, bounding_boxs = self.net(x)
        for i in range(len(class_IDs[0])):
            if class_IDs[0][i] == 0 and scores[0][i] >= self.score:
                temp = bounding_boxs[0][i].asnumpy()
                scale = scale_ratio
                x, y, w, h = temp / scale
                # print(x,y,w,h)
                left = int(x)
                top = int(y)
                right = int(w)
                bottom = int(h)
                return_boxs.append((left, top, right, bottom))
        # current_time = datetime.now().strftime("%H:%M:%S:%f")
        # print(current_time)
        return return_boxs


if __name__ == '__main__':
    gl = GLUON()
    for filename in os.listdir('./images/'):
        if filename.endswith('.jpg'):
            img = cv2.imread('./images/' + filename)

            boxes = gl.detect_image(img)
            for box in boxes:
                x, y, w, h = box
                cv2.rectangle(img, (x, y), (w, h), (0, 255, 255), 1)

            cv2.imshow("Image", img)
            cv2.waitKey(1)

            cv2.imwrite('./results/' + filename, img)
