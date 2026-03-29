from fastapi import  UploadFile
import re
from typing import List, Dict
from textOcr import TextOCR
import io
import fitz  # PyMuPDF
from PIL import Image

class DocumentLoader:
    """Robust PDF loader with OCR fallback"""

    @staticmethod
    def clean_text(text: str) -> str:
        """normalize whitespace and remove special characters."""
        text = re.sub(r'\s+', ' ', text)  #multiple spaces to single space
        text = re.sub(r'[^\w\s\.\,\!\?\-\:\;]', '', text)  #keep punctuation
        return text.strip()

    @staticmethod
    async def load_path(file: UploadFile) -> List[Dict]:
        chunks = []

        try:
            file_bytes = file.file.read()
            doc = fitz.open(stream=file_bytes, filetype="pdf")

            for page_num in range(len(doc)):
                page = doc[page_num]

                #  Step 1: Try normal text extraction
                text = page.get_text().strip()

                # Case 1: Normal PDF
                if text:
                    chunks.append({
                        "text": DocumentLoader.clean_text(text),
                        "metadata": {
                            "source": file.filename,
                            "page": page_num + 1,
                            "type": "text"
                        }
                    })
                    
                    image_list = page.get_images()

                    for item in image_list:
                        xref = item[0]
                        base_image = doc.extract_image(xref)
                        image_bytes = base_image["image"]

                        img = Image.open(io.BytesIO(image_bytes))

                        ocr_text = TextOCR.extract_text_from_image(img)

                        if ocr_text:
                            chunks.append({
                                "text": DocumentLoader.clean_text(ocr_text),
                                "metadata": {
                                    "source": file.filename,
                                    "page": page_num + 1,
                                    "type": "image_ocr"
                                }
                            })

                # 🔥 Case 2: Scanned PDF → full page OCR
                else:
                    print(f"Running OCR on full page {page_num + 1}")

                    pix = page.get_pixmap(dpi=300)  # high resolution

                    img = Image.frombytes(
                        "RGB",
                        [pix.width, pix.height],
                        pix.samples
                    )

                    ocr_text = TextOCR.extract_text_from_image(img)

                    if ocr_text:
                        chunks.append({
                            "text": DocumentLoader.clean_text(ocr_text),
                            "metadata": {
                                "source": file.filename,
                                "page": page_num + 1,
                                "type": "ocr_full_page"
                            }
                        })

                
                

        except Exception as e:
            print(f"error loading PDF {file.filename}: {e}")

        return chunks