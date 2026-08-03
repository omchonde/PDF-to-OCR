import os
import cv2
import numpy as np
from pdf2image import convert_from_path
from PIL import Image

from preprocess import preprocess_image
from ocr_engine import ocr_image_to_words, correct_orientation
from pdf_builder import build_searchable_page, merge_pages_to_pdf

INPUT_PDF = "input/scanned.pdf"
OUTPUT_PDF = "output/searchable.pdf"
DPI = 600  # higher DPI = better OCR accuracy, larger file

def pil_to_cv2(pil_image):
    arr = np.array(pil_image.convert("RGB"))
    return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)

def cv2_to_pil(cv2_image):
    rgb = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb)

def main():
    os.makedirs("output", exist_ok=True)

    print("Converting PDF pages to images...")
    pil_pages = convert_from_path(INPUT_PDF, dpi=DPI)

    page_buffers = []

    for i, pil_page in enumerate(pil_pages):
        print(f"Processing page {i + 1}/{len(pil_pages)}...")

        cv2_page = pil_to_cv2(pil_page)
        cv2_page = correct_orientation(cv2_page)      # fix 90/180/270 first
        _, deskewed_color = preprocess_image(cv2_page)  # then fine-tune skew

        # OpenCV preprocessing
        _, deskewed_color = preprocess_image(cv2_page)

        # Run OCR on the cleaned image
        words = ocr_image_to_words(deskewed_color)

        # PDF page size in points (72 pt = 1 inch)
        img_h_px, img_w_px = deskewed_color.shape[:2]
        page_width_pt = img_w_px * 72 / DPI
        page_height_pt = img_h_px * 72 / DPI

        visible_image = cv2_to_pil(deskewed_color)

        buf = build_searchable_page(
            visible_image, words,
            page_width_pt, page_height_pt,
            img_w_px, img_h_px
        )
        page_buffers.append(buf)

    print("Merging pages into final searchable PDF...")
    merge_pages_to_pdf(page_buffers, OUTPUT_PDF)
    print(f"Done! Output saved to {OUTPUT_PDF}")

if __name__ == "__main__":
    main()