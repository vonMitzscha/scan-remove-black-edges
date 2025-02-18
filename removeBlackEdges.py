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
    """Prüft, ob ein Kontur mindestens drei Bildränder berührt."""
    height, width = img_shape[:2]  
    borders_touched = set()

    for point in contour:
        x, y = point[0]
        if x == 0:  
            borders_touched.add('left')
        elif x == width - 1:  
            borders_touched.add('right')
        elif y == 0:  
            borders_touched.add('top')
        elif y == height - 1:  
            borders_touched.add('bottom')

        if len(borders_touched) >= 2:
            return True

    return False

def feather_alpha_channel(alpha, feather_radius=10, mask_reduction_iterations=2):
    """Verkleinert die Maske leicht, bevor der Weichzeichner angewendet wird, um dunkle Kanten zu vermeiden."""
    kernel_size = (feather_radius * 2 + 1, feather_radius * 2 + 1)
    
    # Maske vorher leicht verkleinern
    alpha = cv2.erode(alpha, np.ones((3, 3), np.uint8), iterations=mask_reduction_iterations)

    # Dann weichzeichnen
    blurred_alpha = cv2.GaussianBlur(alpha, kernel_size, 0)
    
    return blurred_alpha




def make_transparent(input_image_path, output_image_path, threshold=100, min_contour_area=50, feather_radius=5):
    img = cv2.imread(input_image_path)
    if img is None:
        print(f"Fehler beim Laden der Datei: {input_image_path}")
        return

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    mask = np.zeros_like(gray)

    if contours:
        filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]
        for contour in filtered_contours:
            if is_connected_to_three_borders(contour, img.shape):
                cv2.drawContours(mask, [contour], -1, (255), thickness=cv2.FILLED)

    img_rgba = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
    
    # Erstelle einen Alpha-Kanal basierend auf der Maske
    alpha = np.full(mask.shape, 255, dtype=np.uint8)  
    alpha[mask > 0] = 0  # Hintergrund wird transparent gesetzt

    # **Feathering auf den Alpha-Kanal anwenden**
    alpha = feather_alpha_channel(alpha, feather_radius)

    # Setze den Alpha-Kanal in das Bild
    img_rgba[:, :, 3] = alpha  

    Image.fromarray(img_rgba).save(output_image_path, "PNG")

def process_images(input_directory, output_directory, threshold=100, min_contour_area=50, feather_radius=10):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(input_directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
            input_image_path = os.path.join(input_directory, filename)
            output_image_path = os.path.join(output_directory, f"op_{filename}")
            make_transparent(input_image_path, output_image_path, threshold, min_contour_area, feather_radius)
            print(f"Processed: {filename} -> op_{filename}")

# Beispielaufruf
input_dir = "input"  
output_dir = "output"  
process_images(input_dir, output_dir, threshold=100, min_contour_area=10, feather_radius=3)
