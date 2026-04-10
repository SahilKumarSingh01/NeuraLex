from fastapi import FastAPI,File, UploadFile
from typing import Annotated,List
import os
from models.documentLoader import DocumentLoader
import json
import requests
import shutil
from ragSystem import RAGSystem
from fastapi.responses import StreamingResponse
rag=RAGSystem()
app = FastAPI()


@app.post("/uploadFiles")
async def upload_create_file(collectionName:str="default",file1:UploadFile=File(...)):
    
    files:List[UploadFile]=[]
    files.append(file1)
    UPLOAD_DIR = "uploads"

    collection_path=os.path.join(UPLOAD_DIR,collectionName)
    
    if not os.path.exists(collection_path):
        os.makedirs(collection_path)
    
    saved_files = []
    # file_paths=[]
    for file in files:
        
        if not file:
            continue
        
        file_path = os.path.join(collection_path, file.filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        saved_files.append(file.filename)
        
    
    rag.ingest_document(saved_files,collectionName)
     
    return {
        "files": saved_files,
        "status": "saved",
        
        # "chunks": [c.to_dict() for c in chunks]
        
    }

@app.delete("/deleteFiles")
async  def delete_upload_file(files:List[str],collectionName:str="default"):
    
    UPLOAD_DIR = "uploads"

    collection_path=os.path.join(UPLOAD_DIR,collectionName)
    
    if not os.path.exists(collection_path):
        return {
            "files":json.dump(files),
            "status":"deleted"
        }
    
    for file in files:
        file_path=os.path.join(collection_path,file)
        if os.path.exists(file_path):
            os.remove(file_path)
    rag.deleteChunkEmbedding(collectionName,files)
    return {
            "files":json.dumps(files),
            "status":"deleted"
        }
    
@app.post("/generate")
def query(ques:str,sourceFileNameList:List[str],collectionName:str="default"):
    
    def stream():
        itr=rag.query(ques, sourceFileNameList, collectionName)
        llm_response_source_List=itr[0]
        yield json.dumps({"llm_response_source":llm_response_source_List})+'\n'
        
        for chunk in itr[1]:
          yield json.dumps({"llm_response":chunk})+'\n'
          
        
            
    # media_type="application/json"
    # media_type="text/plain"
    return StreamingResponse(stream(), media_type="application/json")

@app.post("/getChunks")
def getChunks(files:List[str],collectionName:str="default"):
    
    chunks=rag.getChunks(collectionName,files)
    
    return {
        "chunks":[c.to_dict() for c in chunks]
    }