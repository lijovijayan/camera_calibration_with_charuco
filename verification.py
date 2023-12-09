import os
import cv2
import numpy as np
import yaml

def loadCameraParams(filename):
    with open(filename, 'r') as file:
        calib_data = yaml.safe_load(file)
        camera_matrix = np.array(calib_data['camera_matrix']['data'])
        distortion_coefficients = np.array(calib_data['distortion_coefficients']['data'])
        return camera_matrix, distortion_coefficients

def undistortImage(image, camera_matrix, distortion_coefficients):
    h, w = image.shape[:2]
    new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, distortion_coefficients, (w, h), 1, (w, h))
    undistorted_image = cv2.undistort(image, camera_matrix, distortion_coefficients, None, new_camera_matrix)
    return undistorted_image

if __name__ == "__main__":
    # Replace 'calibration.yml' with the actual output file name
    calibration_file = 'calibration.yml'
    
    # Load calibration parameters
    camera_matrix, distortion_coefficients = loadCameraParams(calibration_file)

    # Replace 'images_folder' with the path to the folder containing images for verification
    images_folder = 'images'

    # Create an output folder for undistorted images
    output_folder = 'undistorted_images'
    os.makedirs(output_folder, exist_ok=True)

    # Loop through images in the folder
    for image_filename in os.listdir(images_folder):
        if image_filename.endswith(('.jpg', '.jpeg', '.png')):
            # Read the image
            image_path = os.path.join(images_folder, image_filename)
            original_image = cv2.imread(image_path)

            # Undistort the image
            undistorted_image = undistortImage(original_image, camera_matrix, distortion_coefficients)

            # Save undistorted image to the output folder
            output_path = os.path.join(output_folder, f'undistorted_{image_filename}')
            cv2.imwrite(output_path, undistorted_image)

            # Display the original and undistorted images
            cv2.imshow('Original Image', original_image)
            cv2.imshow('Undistorted Image', undistorted_image)
            cv2.waitKey(0)

    cv2.destroyAllWindows()
