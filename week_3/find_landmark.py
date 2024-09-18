# This file is used to find the landmarks (Aruco Marker) in the image plane and drive the robot to the landmark 
# by computing the distance and angle between the robot and the landmark.

# Import the required libraries
import cv2 # Import the OpenCV library
from cv2 import aruco
import numpy as np


def gstreamer_pipeline(capture_width=1024, capture_height=720, framerate=30):
    """Utility function for setting parameters for the gstreamer camera pipeline"""
    return (
        "libcamerasrc !"
        "videobox autocrop=true !"
        "video/x-raw, width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "videoconvert ! "
        "appsink"
        % (
            capture_width,
            capture_height,
            framerate,
        )
    )


print("OpenCV version = " + cv2.__version__)

# Open a camera device for capturing
cam = cv2.VideoCapture(gstreamer_pipeline(), apiPreference=cv2.CAP_GSTREAMER)


if not cam.isOpened(): # Error
    print("Could not open camera")
    exit(-1)

# # Open a window
# WIN_RF = "Example 1"
# cv2.namedWindow(WIN_RF)
# cv2.moveWindow(WIN_RF, 100, 100)

# Get the predefined dictionary
img_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250) # As per the assignment


# Process video frames and check for Aruco markers

while cv2.waitKey(4) == -1: # Wait for a key pressed event
    retval, frameReference = cam.read() # Read frame
    
    if not retval: # Error
        print(" < < <  Game over!  > > > ")
        exit(-1)
    
    # Detect the markers in the images
    corners, ids, _ = aruco.detectMarkers(frameReference, img_dict)

    # If no markers are detected
    if not corners:
        print("No corners detected")
        continue

    # Get the camera matrix and distortion coefficients
    cam_matrix = np.zeros((3, 3))
    coeff_vector = np.zeros(5)

    # Estimate the pose of the markers in the image
    rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, 0.05, cam_matrix, coeff_vector)

    print("rvecs: ", rvecs)
    print("tvecs: ", tvecs)
    

# Finished successfully
