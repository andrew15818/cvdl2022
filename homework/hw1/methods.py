import os
import time
import cv2
import matplotlib

import numpy as np

class Calibration():
    def __init__(self, patternSize=(8,11)):
        self.patternSize = patternSize
        self.corners, self.imgs = [], []
        self.boardSize = self.patternSize[0] * self.patternSize[1]

    # If reading from entire dir, 
    # find corners and show image for 0.5 seconds
    def find_chessboard_corners_dir(self, path):
        # To smoothly display the images, try collecting 
        # them all first then displaying
       
        
        self.successes = 0
        # Loop through images in dir
        for image in os.listdir(path):
            # Join dir path w/ filename and open it
            full_path = os.path.join(path, image)
            img = cv2.imread(full_path, cv2.IMREAD_GRAYSCALE)

            # find corners in each one
            found, corners = cv2.findChessboardCorners(img, 
                                                       self.patternSize)
            filled = cv2.drawChessboardCorners(img, 
                                               self.patternSize,
                                               corners,
                                               found)
            self.successes += 1
            self.corners.append(corners)
            self.imgSize = img.shape[:-1]
            # display the image
            #cv2.imshow(f'{image}', filled)
            #cv2.waitKey(500)
            #cv2.destroyAllWindows()

    def find_intrinsic_matrix(self):
        # Take the corners we found and convert them to 
        # correct format for camera calibration
        imgPoints = np.zeros((self.successes * self.boardSize, 2))
        objPoints = np.zeros((self.successes * self.boardSize, 3))
        
        print(self.corners[0][0][0])
        for curr in range(self.successes):
            step = curr * self.boardSize
            i, j = step, 0
            for j in range(self.boardSize):
                imgPoints[i,0] = self.corners[0][j][0][0]
                imgPoints[i,1] = self.corners[0][j][0][1]
                objPoints[i,0] = j / self.patternSize[1]
                objPoints[i,1] = j % self.patternSize[1]
                objPoints[i,2] = 0

        ret, mtx, dist, rvects, tvecs = \
                cv2.calibrateCamera(objPoints, imgPoints, (2048, 2048), None, None)
