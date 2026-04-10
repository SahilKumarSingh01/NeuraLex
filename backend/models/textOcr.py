import os
import pytesseract
from PIL import Image, ImageFilter
import numpy as np

os.environ["PATH"] += r";C:\Program Files\Tesseract-OCR"
os.environ["TESSDATA_PREFIX"] = r"C:\Program Files\Tesseract-OCR\tessdata"


class TextOCR:
    @staticmethod
    def extract_text_from_image(img) -> str:
        try:
            # Ensure RGB
            if img.mode != "RGB":
                img = img.convert("RGB")

            # PIL preprocessing
            img=img.convert("L")
            img1 = img.filter(ImageFilter.GaussianBlur(radius=5))
            # 🔥 Convert PIL → OpenCV
            img_np1 = np.array(img1)
            img_np2=np.array(img)
                # Create binary image
            binary = (img_np1 < img_np2).astype(np.uint8)

            # Optional: convert 0/1 → 0/255 for visualization
            binary_img = (binary * 255).astype(np.uint8)
           
           
            text = pytesseract.image_to_string(
                binary_img
            )

            return text.strip()

        except Exception as e:
            print(f"OCR error: {e}")
            return ""