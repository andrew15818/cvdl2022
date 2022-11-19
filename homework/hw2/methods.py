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
    while cap.isOpened() and i <= frames:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        volume[i] = gray / 255
        cv2.imshow(f'{i}', volume[i])
        i += 1
    
    # Compute Gaussian parameters across each pixel location
    means = np.mean(volume, axis=0)
    devs = np.std(volume, axis=0)

    cap.release()
    return means, devs 

# Use the first 24 frames to build Gaussian model with mean , stddev
# For the remaining frames, compare pixel value to stddev 
# to check if background, foreground
def subtractBackground(videoPath):

    mean, stddev = buildGaussianModel(videoPath)


