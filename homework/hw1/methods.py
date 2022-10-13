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
            self.imgSize = img.shape[::-1]

            # display the image
            # TODO: Uncomment this for demo
            #cv2.imshow(f'{image}', filled)
            #cv2.waitKey(500)
            #cv2.destroyAllWindows()

    def find_intrinsic_matrix(self):
        # Take the corners we found and convert them to 
        # correct format for camera calibration
        imgPoints = np.zeros((self.successes * self.boardSize, 2), np.float32)
        objPoints = np.zeros((self.successes , self.boardSize, 3), np.float32)

        objPoints[:,:,:2] = np.mgrid[0:self.patternSize[0], 0:self.patternSize[1]].T.reshape(-1, 2)
        
        # Returns: intrinsic matrix, distortion coefficients,
        # rotation & translation vectors from 3d-2d
        ret, self.intrMat, self.distCoeff, self.rotVec, self.transVec= \
                cv2.calibrateCamera(objPoints, self.corners, self.imgSize, None, None)

        print(f'Intrinsic Matrix:\n{self.intrMat}')

