from fastapi import FastAPI, File, UploadFile
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

app = FastAPI()

# =========================
# ✅ CORS (React connect)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# =========================
# ✅ HOME
# =========================
@app.get("/")
def home():
    return {"message": "Backend running 🚀"}


# =========================
# 💬 CHAT API (DUMMY)
# =========================
@app.post("/chat")
def chat(data: dict):
    question = data.get("question")
    files = data.get("files", [])
    mode = data.get("mode", "Normal")

    return {
        "answer": f"Mode: {mode} | Files: {len(files)} | You asked: {question}",
        "summary": "Dummy summary",
        "sources": [
            {"page": 1, "text": "Demo content"}
        ]
    }


# =========================
# 📤 UPLOAD API (IMPORTANT)
# =========================
@app.post("/upload")
def upload_files(files: List[UploadFile] = File(...)):

    uploaded_files = []

    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        # 🔥 overwrite if same name
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        uploaded_files.append(file.filename)

    return {
        "message": "Files uploaded successfully",
        "files": uploaded_files
    }