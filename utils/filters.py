from PIL import Image
import cv2
import numpy as np


def apply_grayscale(image_path):
    """
    Convert image to grayscale
    """
    image = Image.open(image_path).convert("L")
    return image.convert("RGB")


def apply_sepia(image_path):
    """
    Apply sepia filter
    """
    image = Image.open(image_path)
    width, height = image.size
    pixels = image.load()

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]

            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)

            pixels[x, y] = (
                min(255, tr),
                min(255, tg),
                min(255, tb),
            )

    return image


def apply_blur(image_path):
    """
    Apply Gaussian blur
    """
    img = cv2.imread(image_path)
    blurred = cv2.GaussianBlur(img, (15, 15), 0)
    blurred = cv2.cvtColor(blurred, cv2.COLOR_BGR2RGB)
    return Image.fromarray(blurred)


def apply_cartoon(image_path):
    """
    Apply cartoon effect
    """
    img = cv2.imread(image_path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 7)

    edges = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        9,
        9
    )

    color = cv2.bilateralFilter(img, 9, 300, 300)
    cartoon = cv2.bitwise_and(color, color, mask=edges)

    cartoon = cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB)
    return Image.fromarray(cartoon)
