import cv2
import os
import time
from picamera2 import Picamera2


FRAME_SIZES = [
    (426, 240),   # 240p
    (640, 360),   # 360p
    (854, 480),   # 480p
    (1280, 720),  # 720p
    (1920, 1080)  # 1080p
]
FRAME_SIZE = FRAME_SIZES[3]

def init_camera():
    print("Initializing Camera...")

    cam = Picamera2()

    cam.preview_configuration.main.size = FRAME_SIZE
    cam.preview_configuration.main.format = "RGB888"
    cam.preview_configuration.align()
    cam.configure("preview")

    cam.start()

    time.sleep(1)

    print("Initialized Camera...")
    return cam

# Get the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Open the rpi camera
camera = init_camera()
time.sleep(2)

# if not cap.isOpened():
#     print("Error: Could not open camera.")
#     exit()

# Create the 'images' folder in the same directory as the script if it doesn't exist
images_folder = os.path.join(script_dir, "images")
os.makedirs(images_folder, exist_ok=True)

# Initialize index for naming captured images
index = 1

while True:
    # Read a frame from the camera
    frame = camera.capture_array()

    # if not ret:
    #     print("Error: Failed to capture frame.")
    #     break

    # Display the frame
    cv2.imshow("Preview", frame)

    # Check for the 'x' key press
    key = cv2.waitKey(1) & 0xFF
    if key == ord('x'):
        # Save the current frame as an image with the appropriate index in the 'images' folder
        image_filename = os.path.join(images_folder, f"{index}.jpg")
        cv2.imwrite(image_filename, frame)
        print(f"Image {index} captured and saved as {image_filename}")
        index += 1

    # Check for the 'ESC' key press to exit the loop
    elif key == 27:
        break

# Release the camera and close the OpenCV window
cap.release()
cv2.destroyAllWindows()
