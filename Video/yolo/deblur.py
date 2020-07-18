import cv2
import os
import numpy as np

# image = cv2.imread('./results/20200514_191849_472376.jpg')
sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])

for filename in os.listdir('../images/'):
    if filename.endswith('.jpg'):
        img = cv2.imread('../images/' + filename)
        # laplacian_var = cv2.Laplacian(img, cv2.CV_64F).var()
        # if laplacian_var < 5:
        #     print("Blur")
        # print(laplacian_var)
        # cv2.imshow("IG", img)
        # cv2.waitKey(0)

        sharpen = cv2.filter2D(img, -1, sharpen_kernel)
        cv2.imshow('sharpen', sharpen)
        cv2.imwrite('results2/' + filename, sharpen)
        # cv2.waitKey()
cv2.destroyAllWindows()
# cv2.imshow("test", img)
# print("Done ", filename)
