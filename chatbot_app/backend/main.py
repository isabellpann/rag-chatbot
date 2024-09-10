from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import numpy as np

from rag_chatbot import extract_text_from_pdf, load_split, embed_prompt, embed_context, similarity_search, chat_with_bot, generate_response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow only the frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


@app.post("/rag-chat/")
async def rag_chat(question: str = Form(...), pdf_file: UploadFile = File(...)):
    try:
        print(f"Received question: {question}")
        print(f"Received file: {pdf_file}")

        # Embedding
        text = extract_text_from_pdf(pdf_file)
        splits = load_split(text)
        question_embeddings = embed_prompt(question)
        context_embeddings = embed_context(splits)

        # Retrieval
        similarities = similarity_search(question_embeddings, context_embeddings)
        top_indices = np.argsort(similarities, axis=1)[0][-5:]
        relevant_chunks = [splits[i] for i in top_indices]
        context = " ".join(relevant_chunks)

        # Generation
        formatted_prompt = f"Given this context : {context}, {question}."
        response = chat_with_bot(formatted_prompt)

        return {"response": response}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))