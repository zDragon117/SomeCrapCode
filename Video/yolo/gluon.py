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
    img = np.zeros((500, 500, 0), np.uint8)
    image = cv2.imread("74479741_1172606866276646_370400401968594944_o.jpg")

    arra = mx.nd.array(image)
    img_1 = cv2.imread("74479741_1172606866276646_370400401968594944_o.jpg")
    img_1 = cv2.resize(img_1, (416, 740))
    x =  mx.nd.image.to_tensor(arra)
    # x, img = data.transforms.presets.yolo.transform_test(arra)

    print(img.shape)
    print(image.shape)

    cv2.imshow("img", img)
    cv2.imshow("img123", img_1)

    cv2.waitKey(0)
# gl = GLUON()
# # sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
# for filename in os.listdir('../images/'):
#     if filename.endswith('.jpg'):
#         print(filename)
#         img = cv2.imread('../images/' + filename)
#
#         boxes = gl.detect_image(img)
#         for box in boxes:
#             x, y, w, h = box
#             cv2.rectangle(img, (x, y), (w, h), (0, 255, 255), 1)
#         cv2.imwrite('results/' + filename, img)

# cv2.imshow("test", img)
# print("Done ", filename)
#
# zone = np.array([[151, 0],[162, 185],[325, 256],[462, 246],[485, 206],[455, 114],[433, 1]])
# ratio = [1980 / 960, 1080 / 540]
# zone = np.round(zone * ratio).astype(int)
# # print(zone)
# # zone in points: [[392, 3],[400, 160],[474, 175],[654, 274],[711, 102],[960, 183],[960, 1]]
# # zone out points: [[4, 536],[598, 539],[646, 296],[356, 216],[252, 210],[2, 296]]
#
# img = cv2.imread('../images/20200514_191849_472376.jpg')
#
# cv2.fillPoly(img, [zone], (255,255,255))
# cv2.polylines(img, [zone], isClosed=True, color= (0, 0, 255), thickness=1)
# # cv2.pointPolygonTest(zone, ())
# cv2.imshow("Image", img)
# cv2.waitKey(0)
