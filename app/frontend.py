# app/frontend.py

import streamlit as st
import requests
import os

# Backend URL
BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="Simple RAG App")
st.title("Simple RAG App")

# --- Upload Section ---
st.header("Upload a Document")

uploaded_file = st.file_uploader("Choose a document", type=["pdf", "txt", "docx"])

if uploaded_file is not None:
    files = {"file": (uploaded_file.name, uploaded_file, "application/octet-stream")}
    response = requests.post(f"{BACKEND_URL}/upload/", files=files)
    if response.status_code == 200:
        st.success("File uploaded and processed successfully!")
        # Save filename into session
        st.session_state['uploaded_filename'] = uploaded_file.name
    else:
        st.error(f"Failed to upload: {response.text}")

st.divider()

# --- Question Section ---
st.header("Ask a Question")

query = st.text_input("Type your question:")

# Pre-fill file name
default_filename = st.session_state.get('uploaded_filename', '')

file_name = st.text_input("Uploaded file name (auto-filled)", value=default_filename)

if st.button("Ask"):
    if query and file_name:
        params = {"query": query, "file_name": file_name}
        response = requests.post(f"{BACKEND_URL}/search/", params=params)
        if response.status_code == 200:
            result = response.json()
            st.subheader(" Answer:")
            st.write(result["answer"])

            with st.expander("See Retrieved Chunks"):
                for idx, chunk in enumerate(result["results"]):
                    st.markdown(f"**Chunk {idx+1}:** {chunk}")
        else:
            st.error(f"Search failed: {response.text}")
    else:
        st.warning("Please upload a file and type your question first.")
