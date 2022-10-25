import os
import time
import cv2
#import cv2.cv as cv
import matplotlib.pyplot as plt

import numpy as np

            
class Features():
    def __init__(self):
        self.sift = cv2.xfeatures2d.SIFT_create()

    # Find and show the features for single image
    def find_image_features(self, path):
        # Read image in greyscale
        img = cv2.imread(path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Get the keypoints
        kp = self.sift.detect(img, None)
        # draw the keypoints
        featImg = cv2.drawKeypoints(img,
                                    kp,
                                    img
                                    )
        plt.imshow(featImg, 'gray')
        plt.show()
    def match_images(self, img1Path, img2Path):
        img1 = cv2.imread(img1Path)
        img2 = cv2.imread(img2Path)

        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        # Find keypoints and descriptors of both images
        kp1, des1  = self.sift.detectAndCompute(img1, None)
        kp2, des2  = self.sift.detectAndCompute(img2, None)

        # Match keypoints
        matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_FLANNBASED)
        matches = matcher.knnMatch(des1, des2, 2)

        # Check for the best matches
        threshold = 0.60
        goodMatches = []
        for m1, m2 in matches:
            if m1.distance < threshold * m2.distance:
                goodMatches.append([m1])

        # Array where we store two images with matches drawn
        #outImg = np.empty((max(gray1.shape[0], gray2.shape[0]), gray1.shape[1]+gray2.shape[1]))
        matched = cv2.drawMatchesKnn(img1, kp1, img2, kp2, goodMatches, None, flags=2)

        plt.imshow(matched, 'gray')
        plt.show()



