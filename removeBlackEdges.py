#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 21:30:02 2025

@author: marcericmitzscherling
"""

import os
import cv2
import numpy as np
from PIL import Image

def is_connected_to_three_borders(contour, img_shape):
    """Checks if the contour is connected to at least three different image borders."""
    height, width = img_shape[:2]  # Extract height and width only
    borders_touched = set()  # Use a set to store touched borders

    for point in contour:
        x, y = point[0]
        if x == 0:  # Left border
            borders_touched.add('left')
        elif x == width - 1:  # Right border
            borders_touched.add('right')
        elif y == 0:  # Top border
            borders_touched.add('top')
        elif y == height - 1:  # Bottom border
            borders_touched.add('bottom')

        # If two borders are already touched, we can break
        if len(borders_touched) >= 2:
            return True

    return False

def make_transparent(input_image_path, output_image_path, threshold=100, min_contour_area=100, alpha_value=255, blur_radius=3, edge_blur_radius=5):
    # Check if the blur_radius is valid
    if blur_radius <= 0 or blur_radius % 2 == 0:
        raise ValueError("blur_radius must be a positive odd number.")

    # Load image with OpenCV
    img = cv2.imread(input_image_path)
    if img is None:
        print(f"Error loading image: {input_image_path}")
        return

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply threshold to create a binary image
    _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)

    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create a mask for the entire image
    mask = np.zeros_like(gray)  # Mask with black pixels (0)

    # Fill the contours that meet the condition
    if contours:
        filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]
        for contour in filtered_contours:
            if is_connected_to_three_borders(contour, img.shape):
                cv2.drawContours(mask, [contour], -1, (255), thickness=cv2.FILLED)

    # Apply Gaussian Blur to the mask to smooth the edges
    mask = cv2.GaussianBlur(mask, (blur_radius, blur_radius), 0)

    # Weichzeichnen der Kanten der Maske
    mask = cv2.GaussianBlur(mask, (edge_blur_radius, edge_blur_radius), 0)

    # Create a new image with transparency
    img_rgba = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
    img_rgba[:, :, 3] = 255  # Set alpha channel to 255 (fully visible)

    # Set the pixels within the contour to transparent
    img_rgba[mask > 0] = (255, 255, 255, 0)  # Set alpha to 0 for transparent areas

    # Set the alpha for non-masked areas to 255 (fully visible)
    img_rgba[mask == 0, 3] = 255  # Set alpha to 255 for visible areas

    # Save the image
    Image.fromarray(img_rgba).save(output_image_path, "PNG")
 
    
def process_images(input_directory, output_directory, threshold=100, min_contour_area=100):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(input_directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
            input_image_path = os.path.join(input_directory, filename)
            output_image_path = os.path.join(output_directory, f"op_{filename}")
            make_transparent(input_image_path, output_image_path, threshold, min_contour_area)
            print(f"Processed: {filename} -> op_{filename}")

# Example call
input_dir = "input"  
output_dir = "output"  
process_images(input_dir, output_dir, threshold=100, min_contour_area=100)
