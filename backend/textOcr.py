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
            # Convert to grayscale (important for thresholding)
            # gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
            # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            # contrast = clahe.apply(gray)
            # Apply threshold
            # _, thresh = cv2.threshold(
            #     contrast, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
            # )
            # img_np = np.array(img)

            # # Convert to grayscale
            # gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

            # # Blur
            # blur = cv2.GaussianBlur(gray, (5, 5), 0)

            # # Threshold
            # _, thresh = cv2.threshold(
            #     blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
            # )
            # contrast = cv2.adaptiveThreshold(
            # gray,
            # 255,
            # cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            # cv2.THRESH_BINARY,
            # 11,
            # 2
            # )
            # Image.fromarray(contrast).show()
            # Image.fromarray(thresh).show()
            # OCR
            Image.fromarray(binary_img).show()
            text = pytesseract.image_to_string(
                binary_img
            )

            return text.strip()

        except Exception as e:
            print(f"OCR error: {e}")
            return ""