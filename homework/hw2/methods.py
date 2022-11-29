import cv2
import numpy as np

# Return the mean, stddev matrices for first 25 frames
def buildGaussianModel(videoPath, frames=25):
    cap = cv2.VideoCapture(videoPath, cv2.CAP_FFMPEG)
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape

    volume = np.zeros((frames, h, w))
    volume[0] = gray
    i = 1
    while cap.isOpened() and i < frames:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        volume[i] = gray 
        i += 1
    
    # Compute Gaussian parameters across each pixel location
    means = np.mean(volume, axis=0)
    devs = np.std(volume, axis=0)
    devs[devs < 5] = 5

    cap.release()
    return means.astype('uint8'), devs.astype('uint8')

def _get_mask(gray, means, stddevs, mult=5):
    mask = np.zeros(gray.shape)
    excess = np.abs(gray - means)
    
    mask = np.zeros(gray.shape)
    mask[excess > (mult*stddevs)] = 1
    return mask.astype('uint8')

# Use the first 24 frames to build Gaussian model with mean , stddev
# For the remaining frames, compare pixel value to stddev 
# to check if background, foreground
def subtractBackground(videoPath):
    
    # Matrices with means, stddevs for first 25 frames
    means, stddevs = buildGaussianModel(videoPath)
    
    cap = cv2.VideoCapture(videoPath)
    cv2.namedWindow('frame', cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow('mask', cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow('cutout', cv2.WINDOW_AUTOSIZE)
    i = 0
    while cap.isOpened():
        # Skip frames we saw already
        if i < 24:
            i += 1
            continue
        ret, frame = cap.read()

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mask = _get_mask(gray, means, stddevs)

        outFrame = np.ones(shape=gray.shape)
        outFrame = cv2.bitwise_and(gray, mask)

        noBack = np.zeros(frame.shape)
        noBack = np.where(mask==1, frame, 0)
        print(noBack.shape, frame.shape)
        cv2.imshow('frame', frame)
        #cv2.imshow('cutout', noBack)
        cv2.imshow('mask', outFrame*255)
        cv2.waitKey(50)
    cap.release()

def _createDetector():
    params = cv2.simpleBlobDetector_params()
    params.minArea = 35
    params.maxArea = 90
    params.filterByArea = True
    params.minInertiaRatio = 0.9
    params.minConvexity = 0.9
    params.minCircularity = 0.9
    return cv2.SimpleBlobDetector_create(params)

def detectFirstFrame(videoPath):
    cap = cv2.VideoCapture(videoPath)
    ret, frame = cap.read()
    if not ret:
        print('Error reading the frame')
        return

    detector = _createDetector()    
    pass
