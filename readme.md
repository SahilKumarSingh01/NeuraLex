# NeuraLex: Offline RAG System with Ollama

## Overview

This project implements a **Retrieval-Augmented Generation (RAG) system** that allows users to upload documents and ask questions about them.

The system processes documents by:
- Extracting text from uploaded documents
- Splitting the text into smaller chunks
- Creating embeddings for each chunk
- Storing embeddings in a vector database
- Retrieving the most relevant chunks for a query
- Sending the retrieved context to a local LLM using Ollama
- Returning the generated answer to the React frontend

The entire system is designed to **run locally and offline**, ensuring **data privacy and low latency**.

---

## System Architecture

```
User
 │
 ▼
React.js Frontend
 │
 ▼
Backend API
 │
 ├── Document Upload
 │      │
 │      ▼
 │   Text Extraction
 │      │
 │      ▼
 │   Chunk Creation
 │      │
 │      ▼
 │   Embedding Generation
 │      │
 │      ▼
 │   Vector Database (FAISS)
 │
 └── Query Pipeline
        │
        ▼
   Query Embedding
        │
        ▼
 Similarity Search
        │
        ▼
Retrieve Relevant Chunks
        │
        ▼
Send Context + Query to LLM (Ollama)
        │
        ▼
Generated Response
        │
        ▼
React Frontend
```

---

## Features

- Fully **offline RAG pipeline**
- Document upload support
- Automatic **text chunking**
- **Embedding generation**
- **Vector similarity search**
- Local LLM inference using **Ollama**
- React.js frontend for user interaction

---

## Tech Stack

### Backend
- Python
- FAISS (Vector database)
- NumPy
- PyMuPDF / PyPDF2 (PDF parsing)

### LLM Runtime
- Ollama

### Frontend
- React.js

### Embedding Models
- Sentence Transformers / Local embedding models

---

### Install Backend Dependencies

```bash
pip install -r requirements.txt
```
---

### Install Ollama

Follow installation instructions from:

[Ollama Installation Guide](https://ollama.com)

Pull a model:

```bash
ollama pull llama3
```

---


## Future Improvements

- Support for more document formats
- Hybrid search (keyword + vector search)
- Streaming LLM responses
- Better chunk ranking

---

