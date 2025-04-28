# app/main.py

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os

from app import utils
from fastapi import Query

app = FastAPI()

# Directory to save uploaded documents
UPLOAD_DIR = "app/documents"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/search/")
async def search_documents(query: str = Query(...), file_name: str = Query(...)):
    """
    Search the FAISS index for relevant chunks and generate an answer.
    """
    try:
        # Load FAISS index
        index_path = os.path.join(UPLOAD_DIR, f"{file_name}_faiss.index")
        if not os.path.exists(index_path):
            raise HTTPException(status_code=404, detail="FAISS index for the file not found.")
        
        faiss_index = utils.load_faiss_index(index_path)

        # Embed the query
        query_embedding = utils.embedding_model.encode([query]).astype('float32')

        # Search FAISS
        D, I = faiss_index.search(query_embedding, k=3)

        # Get text chunks
        extracted_text = utils.extract_text_from_file(os.path.join(UPLOAD_DIR, file_name))
        text_chunks = utils.chunk_text(extracted_text, chunk_size=500, overlap=50)

        results = []
        for idx in I[0]:
            if idx < len(text_chunks):
                results.append(text_chunks[idx])

        # Generate a final answer
        final_answer = utils.generate_answer(results, query)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "query": query,
        "results": results,
        "answer": final_answer
    }


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    # Accept only PDF or text files
    if not (file.filename.endswith(".pdf") or file.filename.endswith(".txt")):
        raise HTTPException(status_code=400, detail="Only .pdf or .txt files are supported.")

    file_location = os.path.join(UPLOAD_DIR, file.filename)

    # Save the uploaded file
    with open(file_location, "wb") as f:
        content = await file.read()
        f.write(content)

    # Extract, chunk, embed
    try:
        extracted_text = utils.extract_text_from_file(file_location)
        text_chunks = utils.chunk_text(extracted_text, chunk_size=500, overlap=50)
        embeddings = utils.generate_embeddings(text_chunks)
        
        # Create FAISS index
        faiss_index = utils.create_faiss_index(embeddings)
        
        # Save FAISS index (optional, useful for persistence)
        index_save_path = os.path.join(UPLOAD_DIR, f"{file.filename}_faiss.index")
        utils.save_faiss_index(faiss_index, index_save_path)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Respond
    return JSONResponse(content={
        "message": f"File '{file.filename}' uploaded, parsed, chunked, embedded, and FAISS index created!",
        "preview_text": extracted_text[:300],
        "num_chunks": len(text_chunks),
        "num_embeddings": len(embeddings)
    })
