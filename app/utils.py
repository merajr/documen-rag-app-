# app/utils.py

import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from transformers import pipeline

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list:
    """
    Splits text into chunks of `chunk_size` words, with `overlap` between chunks.
    """
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = words[i:i + chunk_size]
        chunks.append(' '.join(chunk))

    return chunks


def extract_text_from_file(file_path: str) -> str:
    """
    Extracts text from a .txt or .pdf file.
    """
    if file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    
    elif file_path.endswith(".pdf"):
        text = ""
        with fitz.open(file_path) as pdf:
            for page in pdf:
                text += page.get_text()
        return text
    
    else:
        raise ValueError("Unsupported file type for text extraction.")

# Load model once (global)
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')


def generate_embeddings(chunks: list) -> list:
    """
    Generates embeddings for a list of text chunks.
    """
    embeddings = embedding_model.encode(chunks)
    return embeddings


def create_faiss_index(embeddings: list) -> faiss.IndexFlatL2:
    """
    Creates a FAISS index and adds the provided embeddings.
    """
    dimension = embeddings[0].shape[0]  # length of embedding vector
    index = faiss.IndexFlatL2(dimension)  # L2 = Euclidean distance

    np_embeddings = np.array(embeddings).astype('float32')  # faiss needs float32
    index.add(np_embeddings)
    
    return index


def save_faiss_index(index: faiss.IndexFlatL2, path: str):
    """
    Saves FAISS index to disk.
    """
    faiss.write_index(index, path)


def load_faiss_index(path: str) -> faiss.IndexFlatL2:
    """
    Loads FAISS index from disk.
    """
    return faiss.read_index(path)


# Load model once (global)
qa_pipeline = pipeline(
    "text2text-generation",
    model="google/flan-t5-small",
    tokenizer="google/flan-t5-small"
)

def generate_answer(context_chunks: list, question: str) -> str:
    """
    Given context and question, generate an answer using a small LLM.
    """
    context = "\n".join(context_chunks)
    prompt = f"Answer the question based on the context:\nContext: {context}\nQuestion: {question}"
    
    output = qa_pipeline(prompt, max_length=200)
    answer = output[0]['generated_text']
    return answer