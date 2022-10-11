import os
import cv2
import matplotlib

# If reading from entire dir, 
# find corners and show image for 0.5 seconds
def find_chessboard_corners_dir(path):
    # Loop through images in dir
    for image in os.listdir(path):
        # Join dir path w/ filename and open it
        full_path = os.path.join(path, image)
        img = cv2.imread(full_path, cv2.IMREAD_GRAYSCALE)
        # find corners in each one
        # display the image
