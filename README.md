# Simple RAG (Retrieval-Augmented Generation) App

A lightweight, production-ready Retrieval-Augmented Generation (RAG) application built with FastAPI (backend) and Streamlit (frontend).  
It allows you to upload documents, generate semantic embeddings, perform vector search with FAISS, and generate natural language answers using a local LLM model.

> **No paid APIs or services required!**  
> **Built 100% free with open-source tools.**

---

## Features

- Upload documents (`.pdf`, `.txt`, `.docx`)
- Parse and chunk documents into smaller text blocks
- Generate embeddings using HuggingFace models
- Store embeddings in a FAISS vector database
- Perform semantic search for best-matching chunks
- Generate final answers using a local LLM model (Flan-T5-small)
- Clean Streamlit UI for uploading files and asking questions
- 100% Free and local — no OpenAI or API key needed

---

## Application Screenshots

![App Screenshot - File Uploading](images/SS1.jpg)

![App Screenshot - Querying from the file](images/SS2.jpg)

---

## Tech Stack

| Layer | Technology |
|:---|:---|
| Backend | FastAPI |
| Frontend | Streamlit |
| Embeddings | HuggingFace Sentence Transformers |
| Vector Store | FAISS |
| Language Model | Flan-T5-small (local model) |
| Programming Language | Python 3.10+ |

---

##  How to Run Locally

### 1. Clone this repository

```
git clone https://github.com/YOUR_USERNAME/simple-rag-app.git
cd simple-rag-app
```

### 2. Install Dependencies

Install everything at once:

```
pip install -r requirements.txt
```

Or manually install:

```
pip install fastapi uvicorn streamlit faiss-cpu sentence-transformers transformers python-docx pdfplumber
```

### 3. Run Backend (FastAPI)

```
uvicorn app.main:app --reload
```

Backend runs at: http://localhost:8000

API docs available at: http://localhost:8000/docs

### 4. Run Frontend (Streamlit)
In another terminal:

```
streamlit run app/frontend.py
```

Frontend runs at: http://localhost:8501

---

## Usage Flow

Upload a document via frontend

System parses and chunks the document

Embeddings are generated and stored in FAISS

Ask a question

Best-matching document chunks are retrieved

Local LLM generates a final natural language answer