import cv2
import os
import sklearn.decomposition as dec
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
   
    cap = cv2.VideoCapture(videoPath)

    ret, old_frame = cap.read()
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)

    keypoints = detectFirstFrame(videoPath, showImage=False)
    p0 = np.array([[kp.pt[0], kp.pt[1]] for kp in keypoints]).astype('float32')
    p0 = np.expand_dims(p0, axis=1)
    #p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)

    if not ret:
        print('Did not capture first frame!')
        return

    mask = np.zeros_like(old_frame) 
    while cap.isOpened():
        ret, frame = cap.read()
        cv2.imshow('hello', frame)
        cv2.waitKey(40)
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
    pts_src = np.float32([[0, 0],
                       [w, 0],
                       [w, h],
                        [0, h],
                ])

    while cap.isOpened():
        ret, frame = cap.read()
        
        (corners, ids, rejected) = cv2.aruco.detectMarkers(frame, arucoDict,
                                                           parameters=arucoParams
                                                           ) 
        #print(f'corners: {corners}, ids: {ids}')
        centers = np.zeros((4, 2)).astype('float32')
        if ids is None:
            print('No ids found:\'(')
            continue
        # What is the role of ids array?
        # Corners gives us the 4 points of the aruco, so get the center
        #for i, corner in enumerate(corners):
        #    centers[i] = corners[i][0][0]
        # Get the coordinates of each point, since they may be detected in different order 
        # And the corresponding point on the target image
        i1 = np.squeeze(np.where(ids == 1))
        rpt1 = np.squeeze(corners[i1[0]])[1]

        i2 = np.squeeze(np.where(ids == 2))
        rpt2 = np.squeeze(corners[i2[0]])[2]

        distance = np.linalg.norm(rpt1 - rpt2)

        scaling = 0.02
        pts_dst = [
                [rpt1[0] - round(scaling * distance), rpt1[1] - round(scaling * distance)]
                ]
        pts_dst = pts_dst + \
                [[rpt2[0] - round(scaling * distance), rpt2[1] - round(scaling * distance)]]


        i3 = np.squeeze(np.where(ids == 3))
        rpt3 = np.squeeze(corners[i3[0]])[0]

        i4 = np.squeeze(np.where(ids == 4))
        rpt4 = np.squeeze(corners[i4[0]])[0]
        
        pts_dst = pts_dst + \
                [[rpt3[0] - round(scaling * distance), rpt3[1] - round(scaling * distance)]]

        pts_dst = pts_dst + \
                [[rpt4[0] - round(scaling * distance), rpt4[1] - round(scaling * distance)]]
        
        pts_dst = np.asarray(pts_dst)
        H, mask = cv2.findHomography(pts_src, pts_dst, cv2.RANSAC, 5.0)
        #H = cv2.getPerspectiveTransform(dstPts, pts_dst)

        warped = cv2.warpPerspective(dstImg, H, (frame.shape[1], frame.shape[0] ))
        
        # Create the mask on the original frame where warped image is placed
        mask = np.zeros([frame.shape[0], frame.shape[1]], dtype=np.uint8)
        cv2.fillConvexPoly(mask, np.int32([pts_dst]), (255, 255, 255), cv2.LINE_AA)

        element = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        mask = cv2.erode(mask, element, iterations=3)

        warped = warped.astype(float)
        mask3 = np.zeros_like(warped)

        print(mask.shape, mask3.shape)
        for  i in range(3):
            mask3[:,:,i] = mask /255
        cv2.imshow('warped', warped) 
        warped_mask = cv2.multiply(warped, mask3)
        masked_frame = cv2.multiply(frame.astype(float), 1-mask3)

        out = cv2.add(warped_mask, masked_frame)
        cv2.imshow('hola', out/255)
        cv2.waitKey(30)
        
    cap.release()

# Use Principal Component Analysis for dimensionality reduction,
# then reconstruct the original input and measure the error
def imageReconstruction(imgPath, components=250):
    pca = dec.PCA(n_components=components)
    losses = []
    for filename in os.listdir(imgPath):
        try:
            img = cv2.imread(os.path.join(imgPath,filename))
            
        except: 
            print(f"Could not read {os.path.join(imgPath, filename)}")
            continue
        
        # Main idea is to perform PCA on each channel separately,
        # then merge for the final image.
        b, g, r = cv2.split(img)

        pca_b = dec.PCA(n_components=components)
        pca_b.fit(b)
        trans_b = pca_b.transform(b)


        pca_g = dec.PCA(n_components=components)
        pca_g.fit(g)
        trans_g = pca_b.transform(g)

        pca_r = dec.PCA(n_components=components)
        pca_r.fit(r)
        trans_r = pca_b.transform(r)

        #print(f'Blue channel variance: {sum(pca_b.explained_variance_ratio_)}')
        #print(f'Green channel variance: {sum(pca_g.explained_variance_ratio_)}')
        #print(f'Red channel variance: {sum(pca_r.explained_variance_ratio_)}')


        # Reconstruct the original image
        b_rec = pca_b.inverse_transform(trans_b)
        g_rec = pca_g.inverse_transform(trans_g)
        r_rec = pca_r.inverse_transform(trans_r)

        rec = cv2.merge((b_rec, g_rec, r_rec)).astype('uint8')
        out = cv2.hconcat([img, rec])

        loss = np.sum((img - rec) ** 2, axis=1).mean()
        losses.append(loss)
        cv2.imshow('final', out)
        cv2.waitKey(50)
    print(losses)
