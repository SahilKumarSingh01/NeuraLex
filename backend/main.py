from fastapi import FastAPI,File, UploadFile
from typing import Annotated
from documentLoader import DocumentLoader

import requests
app = FastAPI()
@app.get("/")
def read_root():
    return {"Hello":"World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.get("/generate")
def generate_text():
    url = "http://localhost:11434/api/generate"
    data={
        "model":"hf.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF:latest",
        "prompt":"explain ollama in 20 words",
        "stream":False
    }
    response=requests.post(url,
                  json=data
                  )
    return {"response":response.json()["response"]}

@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    
    if file.content_type != "application/pdf":
        return {"error": "Only PDF files are supported"}

    chunks = await DocumentLoader.load_path(file)

    return {
        "filename": file.filename,
        "num_chunks": len(chunks),
        "preview": chunks[:]   # optional
    }