import cv2
import os

# Get the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Open the default camera (usually 0, or you can specify a different camera index)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Create the 'images' folder in the same directory as the script if it doesn't exist
images_folder = os.path.join(script_dir, "images")
os.makedirs(images_folder, exist_ok=True)

# Initialize index for naming captured images
index = 1

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture frame.")
        break

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
