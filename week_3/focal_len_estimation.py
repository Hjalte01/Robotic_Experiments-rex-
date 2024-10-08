import cv2 # Import the OpenCV library
from cv2 import aruco
import time
import sys
import numpy as np
from pprint import *

try:
    import picamera2
    print("Camera.py: Using picamera2 module")
except ImportError:
    print("Camera.py: picamera2 module not available")
    exit(-1)

# print("OpenCV version = " + cv2.__version__)

# Open a camera device for capturing
imageSize = (1280, 720)
FPS = 30
cam = picamera2.Picamera2()
frame_duration_limit = int(1/FPS * 1000000) # Microseconds
# Change configuration to set resolution, framerate
picam2_config = cam.create_video_configuration({"size": imageSize, "format": 'RGB888'},
                                                            controls={"FrameDurationLimits": (frame_duration_limit, frame_duration_limit)},
                                                            queue=False)
cam.configure(picam2_config) # Not really necessary
cam.start(show_preview=False)

time.sleep(1)  # wait for camera to setup


# Capture an image from the camera
image = cam.capture_array("main")

print("Image shape: ", image.shape)

# Save the image to a file
cv2.imwrite("aruco_marker.jpg", image)


img_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250) # As per the assignment

# Detect the markers in the images
corners, ids, _ = aruco.detectMarkers(image, img_dict)

corners_board = [tuple(point[0], point[1], 0) for point in corners[0][0]]
corners_board = np.array(corners_board, dtype=np.float32)


if corners == None:
    print("no corners detected")
    sys.exit()

corners = np.array(corners, )

board = aruco.Board_create(corners_board, img_dict, ids)
cam_matrix = np.zeros((3, 3))
coeff_vector = np.zeros(5)


def compute_focal_len_of_image(X, Z, corners):
    """
    The focal length of the camera can be estimated using the formula:
    f = (x * Z) / X
    Parameters:
    - X: Width of the marker in millimeters
    - Z: Distance from the camera to the marker in millimeters
    - corners: Corners of the detected marker in the image plane
    """
    print(corners)
    print(corners[0])
    x = corners[1] - corners[0]  # x difference between the two top corners
    x_diff = x[0]
    return (x_diff * Z) / X

# Measure the width of the marker in millimeters
X = 150


# Measure the distance from the camera to the marker in millimeters
Z = 100



# Compute the focal length of the camera
# compute_focal_len_of_image(X, Z, corners[0][0]) # Corners [0][0] is the first marker detected
# focal_length constant
focal_length = 1694 






_, cam_matrix, coeff_matrix, rvec, tvec = aruco.calibrateCameraAruco(corners, ids, 1, board, imageSize, cam_matrix, coeff_vector)


rvec, tvec, marker_points = aruco.estimatePoseBoard(corners, X, cam_matrix, coeff_vector)

print("\n\ntvec", tvec)

print("\n\nrvec", rvec)

print("\n\nmarker_points", marker_points)

# Save the focal lengths to a file and the corners
# with open("focal_lengths_v2.txt", "a") as f:
#     f.write("Focal length: " + str(focal_length) + "\n")
#     f.write("Distance (Z): " + str(Z) + "\n")
#     f.close()







