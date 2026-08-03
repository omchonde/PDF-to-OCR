import pytesseract
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r"D:\VES\SEM 5 Projects\AID\PDF to OCR\Tesseract-OCR\tesseract.exe"
import cv2

def ocr_image_to_words(image_bgr, lang="eng"):
    """
    Runs Tesseract and returns a list of word dicts:
    {text, left, top, width, height, conf}
    Coordinates are in pixels, relative to the given image.
    """
    rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

    data = pytesseract.image_to_data(
        rgb, lang=lang, output_type=pytesseract.Output.DICT
    )

    words = []
    n = len(data["text"])
    for i in range(n):
        text = data["text"][i].strip()
        conf = int(float(data["conf"][i])) if data["conf"][i] != "-1" else -1
        if text and conf > 0:  # filter out junk/low-confidence noise
            words.append({
                "text": text,
                "left": data["left"][i],
                "top": data["top"][i],
                "width": data["width"][i],
                "height": data["height"][i],
                "conf": conf
            })
    return words

def correct_orientation(image_bgr):
    """Uses Tesseract's OSD to detect 90/180/270 rotation and fix it
    BEFORE fine deskewing. Returns the corrected image."""
    rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(rgb)

    try:
        osd = pytesseract.image_to_osd(pil_img)
        rotation = int([l for l in osd.split("\n") if "Rotate" in l][0].split(":")[-1].strip())
    except Exception:
        rotation = 0

    if rotation == 0:
        return image_bgr

    rot_map = {90: cv2.ROTATE_90_CLOCKWISE,
               180: cv2.ROTATE_180,
               270: cv2.ROTATE_90_COUNTERCLOCKWISE}
    return cv2.rotate(image_bgr, rot_map[rotation])