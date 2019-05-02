
# python barcode-detect.py --image input-images/barcode1.jpg

import numpy as np
import cv2
import argparse
import glob
import os


for filename in glob.iglob('input-images/*.JPG'):
     image = cv2.imread(filename)

     # convert the image to grayscale
     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
     gradX = cv2.Sobel(gray, ddepth = cv2.CV_32F, dx = 1, dy = 0, ksize = -1)
     gradY = cv2.Sobel(gray, ddepth = cv2.CV_32F, dx = 0, dy = 1, ksize = -1)

     # subtract the y-gradient from the x-gradient
     gradient = cv2.subtract(gradX, gradY)
     gradient = cv2.convertScaleAbs(gradient)
     cv2.imshow("Image", gradient)
     cv2.waitKey(0)
     # blur and threshold the image
     blurred = cv2.blur(gradient, (3, 3))
     (_, thresh) = cv2.threshold(blurred, 210, 250, cv2.THRESH_BINARY)
     cv2.imshow("Image", blurred)
     cv2.waitKey(0)
     cv2.imshow("Image", thresh)
     cv2.waitKey(0)
     # construct a closing kernel and apply it to the thresholded image
     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
     closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
     cv2.imshow("Image", kernel)
     cv2.waitKey(0)
     cv2.imshow("Image", closed)
     cv2.waitKey(0)
     # perform a series of erosions and dilations
     closed = cv2.erode(closed, None, iterations = 7)
     cv2.imshow("Image", closed)
     cv2.waitKey(0)
     closed = cv2.dilate(closed, None, iterations = 2)

     cv2.imshow("Image", closed)
     cv2.waitKey(0)

     # find the contours in the thresholded image
     (cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

     # otherwise, sort the contours by area and compute the rotated
     # bounding box of the largest contour
     c = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
     rect = cv2.minAreaRect(c)
     box = cv2.boxPoints(rect)

     cv2.drawContours(image, [box.astype(int)], -1, (0, 255, 0), 3)

     cv2.imshow("Image", image)
     cv2.waitKey(0)

     image_file = 'output-images/' + os.path.basename(filename);
     cv2.imwrite(image_file, image)
