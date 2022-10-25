import os
import time
import cv2
#import cv2.cv as cv
import matplotlib.pyplot as plt

import numpy as np

class Calibration():
    def __init__(self, patternSize=(8,11)):
        self.patternSize = patternSize
        self.corners, self.imgs = [], []
        self.boardSize = self.patternSize[0] * self.patternSize[1]
        self.path = ''

    # If reading from entire dir, 
    # find corners and show image for 0.5 seconds
    def find_chessboard_corners_dir(self, path, show=True):
        # To smoothly display the images, try collecting 
        # them all first then displaying
       
        self.path = path 
        self.successes = 0

        # Loop through images in dir
        for image in os.listdir(path):
            if not image.endswith('.bmp'):
                continue
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
            if show:
                cv2.imshow(f'{image}', filled)
                cv2.waitKey(500)
                cv2.destroyAllWindows()
        return self.corners

    def find_intrinsic_matrix(self):
        # Take the corners we found and convert them to 
        # correct format for camera calibration
        imgPoints = np.zeros((self.successes * self.boardSize, 2), np.float32)
        objPoints = np.zeros((self.successes , self.boardSize, 3), np.float32)

        objPoints[:,:,:2] = np.mgrid[0:self.patternSize[0], 0:self.patternSize[1]].T.reshape(-1, 2)
        print(f'objPoints for intrinsic matrix: {objPoints.shape}') 
        # Returns: intrinsic matrix, distortion coefficients,
        # rotation & translation vectors from 3d-2d
        ret, self.intrMat, self.distCoeff, self.rotVec, self.transVec = \
                cv2.calibrateCamera(objPoints, self.corners, self.imgSize, None, None)
        print(f'Intrinsic Matrix:\n{self.intrMat}')

    # TODO: Correct extrinsic estimation?
    # Make it so that we can find extrinsic matrix for image w/o first finding corners?
    def find_extrinsic_matrix(self, index):
        objPoints = np.zeros((1, self.boardSize, 3), np.float32)

        objPoints[0,:,:2] = np.mgrid[0:self.patternSize[0], 0:self.patternSize[1]].T.reshape(-1, 2)
        retval, rvec, tvec = \
                cv2.solvePnP(objPoints, self.corners[index], self.intrMat, self.distCoeff, np.array(self.rotVec), np.array(self.transVec), useExtrinsicGuess=False)
        ext, jacobian = cv2.Rodrigues(rvec)
        ext = np.append(ext, tvec, axis=1)
        print(f'Extrinsic matrix:\n{ext}')

    def show_distortion(self):
        print(self.distCoeff)

    def show_undistorted(self, index):
        # Open the image
        img = cv2.imread(os.path.join(self.path, f'{index}.bmp'), 
                         cv2.IMREAD_GRAYSCALE)
        
        h, w = img.shape
        newmtx, roi = cv2.getOptimalNewCameraMatrix(self.intrMat, self.distCoeff, (w, h), 1, (w,h) )
        undist = cv2.undistort(img, self.intrMat, self.distCoeff, newmtx)

        cv2.imshow('Distorted eww...', img) 
        cv2.waitKey(0)
        cv2.imshow('Undistorted yay!', undist)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


class Projection():
    def __init__(self, onProjPath='Dataset_CvDl_Hw1/Q2_Image/Q2_lib/alphabet_lib_onboard.txt', 
                 vertProjPath='Dataset_CvDl_Hw1/Q2_Image/Q2_lib/alphabet_lib_vertical.txt'):
        self.onProjPath = onProjPath
        self.vertProjPath = vertProjPath

        self.read_proj_files()
        # First projection part requries calibration
        # Create our own object instead of passing from GUI
        self.cal = Calibration() 

    def read_proj_files(self):
        self.onProjMat = cv2.FileStorage(self.onProjPath, cv2.FILE_STORAGE_READ)
        self.vertProjMat = cv2.FileStorage(self.vertProjPath, cv2.FILE_STORAGE_READ)

    # Each letter has its coordinates for the lines, 
    # Should append all of them together into a single arr
    def gen_word_obj_points(self, word, vert=False):
        objPoints = []
        for letter in word:
            letter = letter.upper()
            if vert:
                objPoints.append(self.vertProjMat.getNode(letter).mat())
            else:
                objPoints.append(self.onProjMat.getNode(letter).mat())
        return np.array(objPoints)
     
    # Have to calibrate before projecting
    def project_on_board(self, imgPath, projectionText):
        corners = self.cal.find_chessboard_corners_dir(imgPath, show=False)

        objPoints = self.gen_word_obj_points(projectionText)
        #objPoints = objPoints.T.reshape(-1,3)
        self.cal.find_intrinsic_matrix()
        print(objPoints.shape, objPoints)
        
        
        r = np.array(self.cal.rotVec)
        rotMat, ext = cv2.Rodrigues(r)
        print(type(objPoints))
        imgPoints, jacobian = cv2.projectPoints(objPoints,
                                                rotMat,
                                                self.cal.transVec,
                                                self.cal.intrMat, 
                                                self.cal.distCoeff)

class Stereo():
    def __init__(self):
        self.mousex = None
        self.mousey = None
        self.disparity = None
    def get_disparity(self, leftImg, rightImg):
        imgL = cv2.imread('Dataset_CvDl_Hw1/Q3_Image/imL.png',0)
        imgR = cv2.imread('Dataset_CvDl_Hw1/Q3_Image/imR.png',0)
        self.leftImg = leftImg
        self.rightImg = rightImg
        stereo = cv2.StereoBM_create(numDisparities=256, blockSize=15)
        self.disparity = stereo.compute(imgL,imgR)
        plt.imshow(self.disparity,'gray')
        plt.show()
        return self.disparity
 
    def get_mouse_coords(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(self.left, (x, y), 10, (255, 0, 0), 10)
            self.mousex = x
            self.mousey = y
            print(self.mousex, self.mousey)
            dispx = self.disparity[self.mousex, self.mousey]
            if dispx == 0:
                return

            corrx = self.mousex + 279
            corry = self.mousey
            cv2.circle(self.right, (corrx, corry), 20, (0, 255, 0), 20)


    def find_corresponding_point(self, ):
        self.left = cv2.imread(self.leftImg)
        self.right = cv2.imread(self.rightImg)

        self.left_gray = cv2.cvtColor(self.left, cv2.COLOR_BGR2GRAY)
        self.right_gray = cv2.cvtColor(self.right, cv2.COLOR_BGR2GRAY)

        r, c = self.left_gray.shape
        # Get image coordinates by clicking
       
        cv2.namedWindow('rightie')
        cv2.namedWindow('leftie')
        cv2.setMouseCallback('leftie', self.get_mouse_coords)
        disparityLeft = np.zeros((r, c), np.float16)
        disparityRight= np.zeros((r, c), np.float16)

        while(1):
            
            cv2.imshow('rightie', self.right)
            cv2.imshow('leftie', self.left)
            # Show corresponding point
            k = cv2.waitKey(27) & 0xFF
            if k == 27:
                break

            # Map to other image
            #FindStereoCorrespondenceGC(self.left, self.right, disparityLeft, disparityRight, state, 0)
            if not self.mousex or not self.mousey:
                continue
            
            #print(f'mouse x, y:{self.mousex, self.mousey}, corr:{dispx-self.mousex, dispx-self.mousey}, {dispx}')

            
class Features():
    def __init__(self):
        self.sift = cv2.SIFT_create()

    # Find and show the features for single image
    def find_image_features(self, path):
        pass
