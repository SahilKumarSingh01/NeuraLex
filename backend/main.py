from fastapi import FastAPI,File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # Import this
from typing import Annotated,List,Dict
import os
from models.documentLoader import DocumentLoader
import json
import requests
import shutil
from ragSystem import RAGSystem
from fastapi.responses import StreamingResponse

rag=RAGSystem()
app = FastAPI()

# Define which origins are allowed to talk to your server
origins = [
    "http://localhost:3000",    # React default
    "http://localhost:5173",    # Vite/Vue default
    "http://127.0.0.1:3000",
    # You can also use ["*"] to allow EVERYTHING, but it's less secure
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],              # Allows all methods (GET, POST, DELETE, etc.)
    allow_headers=["*"],              # Allows all headers
)

@app.post("/uploadFile")
async def upload_create_file(collectionName: str = "default", file: UploadFile = File(...)):
    UPLOAD_DIR = "uploads"
    collection_path = os.path.join(UPLOAD_DIR, collectionName)
    
    if not os.path.exists(collection_path):
        os.makedirs(collection_path)
    
    file_path = os.path.join(collection_path, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    rag.ingest_document([file.filename], collectionName)
     
    return {
        "filename": file.filename,
        "status": "saved",
        "collection": collectionName
    }
    
# In your main.py
@app.get("/listCollections")
def list_collections():
    collections = rag.vector_db.client.list_collections()
    return {"collections": [c.name for c in collections]}

@app.get("/listCollectionFiles")
def list_collection_files(collectionName: str):
    try:
        collection = rag.vector_db.client.get_collection(name=collectionName)
        result = collection.get(include=["metadatas"])
        
        if not result["metadatas"]:
            return {"files": [], "message": "Collection is empty"}

        files = list(set(m.get("source") for m in result["metadatas"] if m))
        return {"files": files}
        
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Collection '{collectionName}' does not exist")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/deleteFiles")
async  def delete_upload_file(files:List[str],collectionName:str="default"):
    
    UPLOAD_DIR = "uploads"

    collection_path=os.path.join(UPLOAD_DIR,collectionName)
    
    if not os.path.exists(collection_path):
        return {
            "files":json.dumps(files),
            "status":"deleted"
        }
    
    for file in files:
        file_path=os.path.join(collection_path,file)
        if os.path.exists(file_path):
            os.remove(file_path)

    # NEW: Delete the folder if it's now empty
    if os.path.exists(collection_path) and not os.listdir(collection_path):
        os.rmdir(collection_path)

    rag.deleteChunkEmbedding(collectionName,files)

    return {
            "files":json.dumps(files),
            "status":"deleted"
        }

@app.post("/chat")
async def chat(messages: List[Dict[str, str]], sourceFileNameList: List[str], collectionName: str = "default", mode: str = "Normal"):
    def stream():
        itr = rag.query(messages, sourceFileNameList, collectionName, mode)
        
        sources = itr[0]
        yield json.dumps({"type": "source", "content": sources}) + '\n'
        
        for chunk in itr[1]:
            yield chunk

    return StreamingResponse(stream(), media_type="application/x-ndjson")

@app.post("/generate")
async def generate(ques: str, sourceFileNameList: List[str], collectionName: str = "default", mode: str = "Normal"):
    def stream():
        messages = [{"role": "user", "content": ques}]
        itr = rag.query(messages, sourceFileNameList, collectionName, mode)
        
        sources = itr[0]
        yield json.dumps({"type": "source", "content": sources}) + '\n'
        
        for chunk in itr[1]:
            yield chunk

    return StreamingResponse(stream(), media_type="application/x-ndjson")

@app.post("/getChunks")
def getChunks(files:List[str],collectionName:str="default"):
    
    chunks=rag.getChunks(collectionName,files)
    
    return {
        "chunks":[c.to_dict() for c in chunks]
    }