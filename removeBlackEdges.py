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
    """Überprüft, ob die Kontur mit mindestens drei verschiedenen Bildrändern verbunden ist."""
    height, width = img_shape[:2]  # Nur Höhe und Breite extrahieren
    borders_touched = set()  # Verwende ein Set, um die berührten Ränder zu speichern

    for point in contour:
        x, y = point[0]
        if x == 0:  # Linker Rand
            borders_touched.add('left')
        elif x == width - 1:  # Rechter Rand
            borders_touched.add('right')
        elif y == 0:  # Oberer Rand
            borders_touched.add('top')
        elif y == height - 1:  # Unterer Rand
            borders_touched.add('bottom')

        # Wenn bereits drei Ränder berührt werden, können wir abbrechen
        if len(borders_touched) >= 2:
            return True

    return False

def make_transparent(input_image_path, output_image_path, threshold=100, min_contour_area=100):
    # Bild mit OpenCV laden
    img = cv2.imread(input_image_path)
    if img is None:
        print(f"Error loading image: {input_image_path}")
        return

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Schwellenwert anwenden, um ein binäres Bild zu erstellen
    _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)

    # Konturen finden
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Erstelle eine Maske für das gesamte Bild
    mask = np.zeros_like(gray)  # Maske mit schwarzen Pixeln (0)

    # Fülle die Konturen, die die Bedingung erfüllen
    if contours:
        filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]
        for contour in filtered_contours:
            if is_connected_to_three_borders(contour, img.shape):
                cv2.drawContours(mask, [contour], -1, (255), thickness=cv2.FILLED)

    # Erstelle ein neues Bild mit Transparenz
    img_rgba = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
    img_rgba[:, :, 3] = 255  # Setze Alpha-Kanal auf 255 (vollständig sichtbar)

    # Setze die Pixel innerhalb der Kontur auf transparent
    img_rgba[mask == 255] = (255, 255, 255, 0)  # Transparent

    # Speichere das Bild
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

# Beispielaufruf
input_dir = "input"  
output_dir = "output"  
process_images(input_dir, output_dir, threshold=100, min_contour_area=100)
