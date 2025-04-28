# app/main.py

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os

from app import utils

app = FastAPI()

# Directory to save uploaded documents
UPLOAD_DIR = "app/documents"
os.makedirs(UPLOAD_DIR, exist_ok=True)

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

    try:
        extracted_text = utils.extract_text_from_file(file_location)
        text_chunks = utils.chunk_text(extracted_text, chunk_size=500, overlap=50)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # (Optional: Return number of chunks for now)
    return JSONResponse(content={
        "message": f"File '{file.filename}' uploaded, parsed, and chunked successfully!",
        "preview_text": extracted_text[:300],
        "num_chunks": len(text_chunks)
    })
