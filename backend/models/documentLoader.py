from fastapi import  UploadFile
import re
from typing import List, Dict
from models.textOcr import TextOCR
import io
import fitz  # PyMuPDF
from PIL import Image
from  schema.chunk import Chunk
import math
import os
from concurrent.futures import ThreadPoolExecutor

class DocumentLoader:
    """Robust PDF loader with OCR fallback"""
    def __int__(self):
        pass
    @staticmethod
    def clean_text(text: str) -> str:
        """normalize whitespace and remove special characters."""
        text = re.sub(r'\s+', ' ', text) 
        text = re.sub(r'[^\w\s\.\,\!\?\-\:\;]', '', text)  
        return text.strip()
    @staticmethod
    def load_file(collectionName:str,fileName:str):
        
        UPLOAD_DIR = "uploads"
        collection_path=os.path.join(UPLOAD_DIR,collectionName)
        file_path=os.path.join(collection_path,fileName)
        
        if os.path.exists(file_path):
            with open(file_path,"rb") as file:
                return file.read()
        return None
    
    def process_page(self,page_num,doc,fileName,file_path,chunk_idx_start)->Chunk:
        
        chunks=[]
        page = doc[page_num]
        #  Step 1: Try normal text extraction
        text = page.get_text().strip()
        chunk_idx=chunk_idx_start
        # Case 1: Normal PDF
        if text:
            chunk_idx=chunk_idx+1
            chunks.append(Chunk(
                id=fileName+"_"+str(chunk_idx),
                text=DocumentLoader.clean_text(text),
                vector=None,
                metadata={
                    "source": fileName,
                    "page": page_num + 1,
                    "type": "text",
                    "filePath":file_path
                }
            ))
            
            image_list = page.get_images()

            for item in image_list:
            
                xref = item[0]
                base_image = doc.extract_image(xref)
                if base_image["width"] < 100 or base_image["height"] < 100: continue
                image_bytes = base_image["image"]

                img = Image.open(io.BytesIO(image_bytes))

                ocr_text = TextOCR.extract_text_from_image(img)

                if ocr_text:
                    
                    chunk_idx=chunk_idx+1
                    chunks.append(Chunk(
                    id=fileName+"_"+str(chunk_idx),
                    text=DocumentLoader.clean_text(ocr_text),
                    vector=None,
                    metadata={
                        "source": fileName,
                        "page": page_num + 1,
                        "type": "image_ocr",
                        "filePath":file_path
                    }
                    ))

            # Case 2: Scanned PDF → full page OCR
            else:
                

                pix = page.get_pixmap(dpi=300)  # high resolution

                img = Image.frombytes(
                    "RGB",
                    [pix.width, pix.height],
                    pix.samples
                )

                ocr_text = TextOCR.extract_text_from_image(img)
                
                if ocr_text:
                    
                    chunk_idx=chunk_idx+1
                    chunks.append(Chunk(
                    id=fileName+"_"+str(chunk_idx),
                    text=DocumentLoader.clean_text(ocr_text),
                    vector=None,
                    metadata={
                        "source": fileName,
                        "page": page_num + 1,
                        "type": "text",
                        "filePath":file_path
                    }
                ))
                    
                    
        return chunks[0]
    
    
    def processFileToChunks(self,fileNameList:List[str],collectionName:str="default") -> List[Chunk]:
        chunks:List[Chunk] = []
        UPLOAD_DIR = "uploads"
        collection_path=os.path.join(UPLOAD_DIR,collectionName)
        
        with ThreadPoolExecutor (max_workers=4) as executor:
            try:
                for fileName in fileNameList:
                    file_bytes=  DocumentLoader.load_file(collectionName,fileName)
                    if file_bytes==None: continue
                    ext=fileName.split(".")[1]
                    file_path = "file:///"+os.path.abspath(os.path.join(collection_path, fileName)).replace("\\","/")
                
                    doc = fitz.open(stream=file_bytes, filetype=ext)
                    
                    pageChunks=[executor.submit(self.process_page,i ,doc,fileName,file_path,i*10) for i in range(len(doc))]
                    
                    for chunk in pageChunks:
                        # print(chunk.result())
                        chunks.append(chunk.result())

            except Exception as e:
              print(f"error loading PDF : {e}")

        return chunks