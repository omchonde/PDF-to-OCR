import cv2
import numpy as np

def deskew(image):
    """Detects skew angle using Hough line detection on text edges,
    which is far more reliable than minAreaRect for real documents."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    lines = cv2.HoughLinesP(
        edges, 1, np.pi / 180,
        threshold=200, minLineLength=image.shape[1] // 3, maxLineGap=20
    )

    if lines is None:
        return image  # nothing detected, don't rotate at all

    angles = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
        # Only keep near-horizontal lines (text lines), ignore verticals/diagonals
        if -20 < angle < 20:
            angles.append(angle)

    if not angles:
        return image

    median_angle = np.median(angles)

    # Safety clamp: don't "correct" tiny noise or wildly wrong detections
    if abs(median_angle) < 0.1 or abs(median_angle) > 15:
        return image

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, median_angle, 1.0)
    rotated = cv2.warpAffine(
        image, M, (w, h),
        flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE
    )
    return rotated


def denoise_and_binarize(image):
    """Grayscale -> denoise -> adaptive threshold for crisp text edges."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray, h=30)

    # Adaptive threshold works better than global threshold for uneven lighting
    binary = cv2.adaptiveThreshold(
        denoised, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        blockSize=31, C=15
    )
    return binary


def preprocess_image(image_bgr):
    """Full preprocessing pipeline: deskew -> denoise -> binarize."""
    deskewed = deskew(image_bgr)
    cleaned = denoise_and_binarize(deskewed)
    # Convert back to 3-channel so downstream tools (Tesseract) are happy
    cleaned_bgr = cv2.cvtColor(cleaned, cv2.COLOR_GRAY2BGR)
    return cleaned_bgr, deskewed