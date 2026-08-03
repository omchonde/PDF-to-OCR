# PDF to Searchable OCR PDF

Converts scanned / image-based PDFs into fully **searchable PDFs** — preserving the original visual layout while making the text selectable, searchable, and copyable.

Built with **OpenCV** for image preprocessing and **Tesseract OCR** for text recognition, with an invisible text layer generated using **ReportLab** and merged back onto the original page using **pypdf**.

---

## ✨ Features

- 📄 Converts multi-page PDFs into images and back into a single merged PDF
- 🧭 Automatic orientation correction (90° / 180° / 270°) using Tesseract OSD
- 📐 Skew detection and correction using Hough Line Transform
- 🧹 Image cleanup — denoising and adaptive/Otsu binarization to boost OCR accuracy
- 🔤 Word-level OCR with bounding box extraction (pytesseract)
- 👻 Invisible, pixel-aligned text layer overlaid on the original scanned image
- ✅ Output PDF looks identical to the original scan, but is fully searchable

---

## 🛠 Tech Stack

| Purpose | Library |
|---|---|
| Image preprocessing | OpenCV |
| OCR engine | Tesseract (via pytesseract) |
| PDF → image conversion | pdf2image (Poppler) |
| Invisible text layer generation | ReportLab |
| PDF merging | pypdf |

---

## 📁 Project Structure

```
pdf-to-searchable-ocr/
├── main.py           # Orchestrates the full pipeline
├── preprocess.py      # OpenCV: deskew, denoise, binarize
├── ocr_engine.py       # Tesseract OCR + orientation correction
├── pdf_builder.py       # Invisible text layer + PDF merging
├── requirements.txt
├── input/               # Place source scanned PDFs here
└── output/               # Searchable PDFs are generated here
```

---

## ⚙️ Setup

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/pdf-to-searchable-ocr.git
cd pdf-to-searchable-ocr
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Install system dependencies

**Tesseract OCR**
- Windows: install from [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki), then set the path in `ocr_engine.py`:
  ```python
  pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
  ```
- macOS: `brew install tesseract`
- Linux: `sudo apt-get install tesseract-ocr`

**Poppler** (required by pdf2image)
- Windows: download from [poppler-windows releases](https://github.com/oschwartz10612/poppler-windows/releases), extract, and either add `Library/bin` to your system PATH, or pass the path directly in `main.py`:
  ```python
  convert_from_path(INPUT_PDF, dpi=DPI, poppler_path=r"C:\poppler\Library\bin")
  ```
- macOS: `brew install poppler`
- Linux: `sudo apt-get install poppler-utils`

---

## ▶️ Usage

1. Place your scanned PDF inside the `input/` folder, e.g. `input/scanned.pdf`
2. Run:
   ```bash
   python main.py
   ```
3. Find the searchable output at `output/searchable.pdf`

### Verify it worked

```bash
pdftotext output/searchable.pdf - | head -30
```

If readable text prints out, the OCR text layer was embedded successfully. You can also open the PDF and try `Ctrl+F` to search for a word.

---

## 🧠 How It Works

1. **PDF → Images**: Each page is rendered to an image using `pdf2image`
2. **Orientation Correction**: Tesseract's OSD detects if a page is rotated 90/180/270° and corrects it
3. **Deskewing**: A Hough Line Transform detects the dominant text line angle and rotates the page to straighten it
4. **Preprocessing**: Denoising and binarization clean up the image for better OCR accuracy
5. **OCR**: Tesseract extracts each word along with its exact pixel coordinates
6. **Invisible Text Layer**: ReportLab draws each recognized word as invisible text (render mode 3) at the exact position it appears in the image
7. **Merge**: The invisible text layer is merged with the visible scanned image using pypdf, page by page
8. **Output**: All pages are combined into one final searchable PDF

---

## 🚧 Known Limitations / Future Improvements

- OCR accuracy depends heavily on scan quality and DPI (300+ recommended)
- Currently supports single-language OCR by default (multi-language support via Tesseract language packs is possible)
- Large batch processing could be parallelized for speed
- Could add a CLI (`argparse`) for configurable input/output paths and DPI

---

## 📸 Example
- Before
  <img width="1920" height="1098" alt="image" src="https://github.com/user-attachments/assets/de067e96-096c-4dc9-83bd-ac29399757ec" />

- After
  <img width="1920" height="1095" alt="image" src="https://github.com/user-attachments/assets/bcacefa4-7001-46eb-a5c6-c2de922e3f91" />



---

## 📄 License

MIT License — feel free to use and modify.
