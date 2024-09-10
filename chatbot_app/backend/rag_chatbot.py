import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import ollama

# embedding model
model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}
hf = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
    )

# llm
huggingfacehub_api_token = "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"
llm = HuggingFaceEndpoint(repo_id='tiiuae/falcon-7b-instruct', huggingfacehub_api_token=huggingfacehub_api_token)


def extract_text_from_pdf(pdf_file):
    # Open the PDF file
    doc = fitz.open(stream=pdf_file.file.read(), filetype="pdf")
    text = ""
    # Extract text from each page
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

def load_split(pdf_text: str):
    # Split the PDF text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
    separators=[
        "\n\n",
        "\n\n\n",
        "\n",
        " ",
        ".",
        ",",
        "\u200b",  # Zero-width space
        "\uff0c",  # Fullwidth comma
        "\u3001",  # Ideographic comma
        "\uff0e",  # Fullwidth full stop
        "\u3002",  # Ideographic full stop
        "",
    ],
    chunk_size=100,
    chunk_overlap=20,
    length_function=len,
    )
    splits = text_splitter.split_text(pdf_text)
    return splits

def embed_context(splits):
    # Generate embeddings for each chunk
    embeddings = np.array(hf.embed_documents(splits))
    return embeddings

def embed_prompt(question):
    # Generate embeddings for the question
    embeddings = np.array(hf.embed_query(question))
    return embeddings

def similarity_search(question_embeddings, context_embeddings):
    return cosine_similarity(question_embeddings.reshape(1, -1), context_embeddings)

def chat_with_bot(input):
    output = llm.invoke(input)
    return output

def generate_response(input):
    response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content':input}])
    return response['message']['content']