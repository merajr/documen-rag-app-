# Simple RAG App

A Python FastAPI app where:

User uploads a document (e.g., a PDF or text).

We store the embeddings of the document chunks.

User asks a question.

We retrieve the most relevant document chunks.

We send the question + relevant chunks to an LLM to generate a smart answer.
