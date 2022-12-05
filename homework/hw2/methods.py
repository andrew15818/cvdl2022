import cv2
import numpy as np

# Return the mean, stddev matrices for first 25 frames
def buildGaussianModel(videoPath, frameCount=25):
    cap = cv2.VideoCapture(videoPath, cv2.CAP_FFMPEG)
    frames = []

    i = 0
    while cap.isOpened() and i < frameCount:
        ret, frame = cap.read()
        if not ret:
            print('Failed to read frame for Gaussian model.')
            return 
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frames.append(frame)
        i += 1
        
    frames = np.array(frames)
    means = np.mean(frames, axis=0)
    devs = np.std(frames, axis=0)
    devs[devs < 5] = 5
    return means, devs

def _get_mask(gray, means, stddevs, mult=5):
    excess = np.abs(gray - means)
    
    mask = np.zeros_like(gray)
    mask[excess > (mult*stddevs)] = 255
    return mask.astype('uint8')

# Use the first 24 frames to build Gaussian model with mean , stddev
# For the remaining frames, compare pixel value to stddev 
# to check if background, foreground
def subtractBackground(videoPath):
    
    # Matrices with means, stddevs for first 25 frames
    means, stddevs = buildGaussianModel(videoPath)
    
    cap = cv2.VideoCapture(videoPath)
    i = 0
   
    while cap.isOpened():
        # Skip frames we saw already
        if i < 24:
            i += 1
            continue
        ret, frame = cap.read()

        if not ret:
            break
        masked = np.zeros_like(frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mask = _get_mask(gray, means, stddevs)
        print(means[100:, 100:], stddevs[100:, 100:])
        for i in range(3):
            masked[:,:,i] = mask

        outFrame = np.ones(shape=gray.shape).astype('uint8')
        outFrame = cv2.bitwise_and(frame, frame, mask= mask)
        out = cv2.hconcat([frame, masked, outFrame])
        cv2.imshow('out', out)
        cv2.waitKey(50)
    cap.release()

def _createDetector():

    params = cv2.SimpleBlobDetector_Params()
    params.minArea = 35
    params.maxArea = 90
    params.filterByArea = True
    params.minInertiaRatio = 0.7
    params.minConvexity = 0.7
    params.minCircularity = 0.7
    return cv2.SimpleBlobDetector_create(params)

def detectFirstFrame(videoPath, showImage=True):
    offset = 5
    cap = cv2.VideoCapture(videoPath)
    ret, frame = cap.read()
    if not ret:
        print('Error reading the frame')
        return

    detector = _createDetector()    
    keypoints = detector.detect(frame) 
    for k in keypoints:
        frame = cv2.rectangle(frame, (int(k.pt[0]-offset), int(k.pt[1]-offset)), (int(k.pt[0]+offset), int(k.pt[1]+offset)), (0, 0, 255), 2)
        frame = cv2.line(frame, (int(k.pt[0])-offset, int(k.pt[1])), (int(k.pt[0] + offset), int(k.pt[1])), (255, 0, 0), 1)
        frame = cv2.line(frame, (int(k.pt[0]), int(k.pt[1]-offset)), (int(k.pt[0]), int(k.pt[1]+offset)), (255, 0, 0), 1)
        #frame = cv2.line()

    if showImage:
        cv2.imshow('frame', frame)
    cap.release()
    return keypoints

# Calculate motion of objects through a video
def opticalFlow(videoPath):
    # Parameters for flow algorithm
    params = {'winSize': (15, 15),
              'maxLevel': 2,
              'criteria' : (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, .03)
            }

    feature_params =  dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)
    # Get the initial coordinates of points
    #keypoints = detectFirstFrame(videoPath, showImage=False)
    #keypoints = np.array([[kp.pt[0], kp.pt[1]] for kp in keypoints])
   
    cap = cv2.VideoCapture(videoPath)

    ret, old_frame = cap.read()
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    keypoints = detectFirstFrame(videoPath, showImage=False)
    p0 = np.array([[kp.pt[0], kp.pt[1]] for kp in keypoints])
    #p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)
    if not ret:
        print('Did not capture first frame!')
        return

    mask = np.zeros_like(old_frame) 
    while cap.isOpened():
        ret, frame = cap.read()
        cv2.imshow('hello', frame)
        cv2.waitKey(50)
        if not ret:
            print('Did not capture image!')
            return

        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Calculate the optical flow
        p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, 
                                               p0, None, **params)
        # Use only the good points
        if p1 is not None:
            good_new = p1[st == 1]
            good_old = p0[st==1]

        for i, (new, old) in enumerate(zip(good_new, good_old)):
            a, b = new.ravel()
            c, d = old.ravel()
            mask = cv2.line(mask, (int(a), int(b)), (int(c), int(d)), (255, 0, 0), 2)
            frame = cv2.circle(frame, (int(a), int(b)), 5, (255, 0, 0), -1)
        img = cv2.add(frame, mask)
        cv2.imshow('holis', img)
        cv2.waitKey(50)

        old_gray = frame_gray.copy()
        p0 = good_new.reshape(-1, 1, 2)
    cap.release()

def perspectiveTransform(videoPath, imgPath):
    cap = cv2.VideoCapture(videoPath)
    # dict of aruco shapes and params
    arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
    arucoParams = cv2.aruco.DetectorParameters_create()
    dstImg = cv2.imread(imgPath)
    h, w, d = dstImg.shape
    dstPts = np.array([[0, 0],
                       [h-1, 0],
                       [0, w-1],
                       [h-1, w-1],
                ])

    while cap.isOpened():
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        
        (corners, ids, rejected) = cv2.aruco.detectMarkers(frame, arucoDict,
                                                           parameters=arucoParams
                                                           ) 
        print(f'corners: {corners}, ids: {ids}, rejected: {rejected}')
        centers = np.zeros((4, 2)).astype('float32')
        if  len(corners) != 4:
            continue
        # What is the role of ids array?
        # Corners gives us the 4 points of the aruco, so get the center
        for i, corner in enumerate(corners):
            centers[i] = corners[ids[i]][0][0]#np.mean(corner, axis=1)
        H, mask = cv2.findHomography(centers, dstPts, cv2.RANSAC, 5.0)
        #H = cv2.getPerspectiveTransform(dstPts, centers)
        warped = cv2.warpPerspective(dstImg, H, (h, w))
        cv2.imshow('warpie', warped)
        cv2.waitKey(50)
    cap.release()
