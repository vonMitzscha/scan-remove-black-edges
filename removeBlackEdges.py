#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 21:09:19 2025

@author: marcericmitzscherling
"""

import os
import cv2
import numpy as np
from PIL import Image

def make_transparent(input_image_path, output_image_path, threshold=100):
    # Bild mit OpenCV laden
    img = cv2.imread(input_image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Schwellenwert anwenden, um ein binäres Bild zu erstellen
    _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)

    # Konturen finden
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Erstelle eine Maske für das gesamte Bild
    mask = np.zeros_like(gray)  # Maske mit schwarzen Pixeln (0)

    # Fülle die größte Kontur (das Dokument) mit Weiß (255)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        cv2.drawContours(mask, [largest_contour], -1, (255), thickness=cv2.FILLED)

    # Erstelle ein neues Bild mit Transparenz
    img_rgba = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
    img_rgba[:, :, 3] = 255  # Setze Alpha-Kanal auf 255 (vollständig sichtbar)

    # Setze die Pixel innerhalb der Kontur auf transparent
    img_rgba[mask == 255] = (255, 255, 255, 0)  # Transparent

    # Speichere das Bild
    Image.fromarray(img_rgba).save(output_image_path, "PNG")

def process_images(input_directory, output_directory, threshold=100):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(input_directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_image_path = os.path.join(input_directory, filename)
            output_image_path = os.path.join(output_directory, f"op_{filename}")
            make_transparent(input_image_path, output_image_path, threshold)
            print(f"Processed: {filename} -> op_{filename}")

# Beispielaufruf
input_dir = "input"  # Ersetze dies durch den Pfad zu deinem Eingabeverzeichnis
output_dir = "output"  # Ersetze dies durch den Pfad zu deinem Ausgabeverzeichnis
process_images(input_dir, output_dir, threshold=100)

