import cv2
import numpy as np
import imutils

# read image
img = cv2.imread('AIP logo.png')

cv2.imshow("ori", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

ht, wd, cc= img.shape
print(ht, wd, cc)
# create new image of desired size and color (blue) for padding
ww = wd + 50
hh = wd + 50
color = (255,255,255)
result = np.full((hh,ww,cc), color, dtype=np.uint8)

# compute center offset
xx = (ww - wd) // 2
yy = (hh - ht) // 2

# copy img image into center of result image
result[yy:yy+ht, xx:xx+wd] = img

# resize image to 512x512
result = imutils.resize(result, width=512)

# view result
cv2.imshow("result", result)
cv2.waitKey(0)
cv2.destroyAllWindows()

# save result
cv2.imwrite("AIP logo 512x512.png", result)