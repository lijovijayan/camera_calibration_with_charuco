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
FRAME_SIZE = FRAME_SIZES[4]

def init_camera():
    print("Initializing Camera...")

    cam = Picamera2()

    # Configure the camera
    config = cam.create_preview_configuration(main={"size": FRAME_SIZE, "format": "RGB888"})
    cam.configure(config)

    # Enable autofocus with supported settings
    cam.set_controls({
        "AfMode": 2,  # 2 = Auto mode
        "AfTrigger": 0,  # 0 = Start AF
        "AfSpeed": 1,  # 1 = Normal speed
        "AfRange": 0,  # 0 = Full range
    })
    
    cam.start()
    time.sleep(2)  # Give more time for autofocus to initialize

    print("Initialized Camera...")
    return cam

# Get the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Open the rpi camera
camera = init_camera()
time.sleep(1)

# if not cap.isOpened():
#     print("Error: Could not open camera.")
#     exit()

# Create the 'images' folder in the same directory as the script if it doesn't exist
images_folder = os.path.join(script_dir, "images")
os.makedirs(images_folder, exist_ok=True)

# Initialize index for naming captured images
index = 1

print("\nCamera is ready!")
print("Press Enter to capture an image")
print("Type 'q' and press Enter to quit\n")

while True:
    # Read a frame from the camera
    frame = camera.capture_array()
    
    # Wait for user input
    user_input = input("Press Enter to capture (or 'q' to quit): ")
    
    if user_input.lower() == 'q':
        break
    
    # Save the current frame as an image with the appropriate index in the 'images' folder
    image_filename = os.path.join(images_folder, f"{index}.jpg")
    cv2.imwrite(image_filename, frame)
    print(f"✓ Image {index} captured and saved as {image_filename}")
    index += 1

# Clean up
camera.stop()
print("\nCamera stopped. Goodbye!")
