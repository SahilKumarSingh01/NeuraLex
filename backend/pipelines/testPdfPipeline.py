import fitz  # PyMuPDF
import spacy
import os
from typing import List, Dict
from CoreferenceResolver import CoreferenceResolver

# ================= 2. THE PDF LOADER =================
class SimplePDFLoader:
    @staticmethod
    def load_pdf(file_path: str) -> List[Dict]:
        chunks = []
        print(f"Reading PDF: {file_path}...")

        try:
            doc = fitz.open(file_path)
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text().strip()

                if text:
                    clean_text = text.replace('\n', ' ')
                    chunks.append({
                        "text": clean_text,
                        "metadata": {
                            "source": file_path,
                            "page": page_num + 1
                        }
                    })

        except Exception as e:
            print(f"Error reading PDF: {e}")

        return chunks


# ================= 3. TEST GENERATOR =================
def create_dummy_pdf(filename="sample_test.pdf"):
    doc = fitz.open()
    page = doc.new_page()

    text = (
        "Alice and Bob went to the tech conference in Paris. \n"
        "They loved the city.\n\n"
        "The senior engineers fixed the massive database server. \n"
        "They were completely exhausted.\n\n"
        "Microsoft released the new Windows update. \n"
        "It became very popular among developers."
    )

    page.insert_text((50, 50), text, fontsize=12)
    doc.save(filename)
    doc.close()
    return filename


# ================= EXECUTION =================
if __name__ == "__main__":

    # pdf_file = create_dummy_pdf()
    pdf_file = "test.pdf"

    # 1. Load PDF
    extracted_pages = SimplePDFLoader.load_pdf(pdf_file)

    # 2. Run improved pipeline
    pipeline = CoreferenceResolver()
    resolved_pages = pipeline.resolve_chunk_pairs(extracted_pages)

    # 3. Print results
    for i in range(len(extracted_pages)):
        print("\n--- ORIGINAL TEXT ---")
        print(extracted_pages[i]["text"])

        print("\n--- RESOLVED TEXT ---")
        print(resolved_pages[i]["text"])