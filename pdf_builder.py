import io
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from pypdf import PdfReader, PdfWriter

def build_searchable_page(image_bgr_rgb_pil, words, page_width_pt, page_height_pt, img_width_px, img_height_px):
    """
    Creates a single-page PDF with:
    - the visible scanned image
    - an invisible text layer aligned to OCR word boxes
    Returns PDF bytes for this page.
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=(page_width_pt, page_height_pt))

    # 1. Draw the visible image covering the full page
    img_reader = ImageReader(image_bgr_rgb_pil)
    c.drawImage(img_reader, 0, 0, width=page_width_pt, height=page_height_pt)

    # 2. Scale factors: pixel coords -> PDF point coords
    scale_x = page_width_pt / img_width_px
    scale_y = page_height_pt / img_height_px

    # 3. Overlay invisible text at each word's position
    c.setFillColorRGB(0, 0, 0)
    for w in words:
        text = w["text"]
        left = w["left"] * scale_x
        top = w["top"] * scale_y
        width = w["width"] * scale_x
        height = w["height"] * scale_y

        # PDF y-axis starts at bottom, image y starts at top
        pdf_y = page_height_pt - top - height

        font_size = max(height * 0.85, 1)
        c.setFont("Helvetica", font_size)

        text_obj = c.beginText(left, pdf_y)
        text_obj.setTextRenderMode(3)  # 3 = invisible text (still selectable/searchable)
        text_obj.textOut(text)
        c.drawText(text_obj)

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer


def merge_pages_to_pdf(page_buffers, output_path):
    """Combines multiple single-page PDF buffers into one final PDF."""
    writer = PdfWriter()
    for buf in page_buffers:
        reader = PdfReader(buf)
        writer.add_page(reader.pages[0])

    with open(output_path, "wb") as f:
        writer.write(f)