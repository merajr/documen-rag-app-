# app/utils.py

import fitz  # PyMuPDF

# app/utils.py (add this)

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
