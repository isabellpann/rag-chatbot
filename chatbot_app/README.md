## Backend Set Up
1. Set up virtual environment

```
cd backend
uv venv
source .venv/bin/activate
```
2. Install requirements
```
uv pip install -r requirements.txt
pip install -r requirements.txt
```
3. Run the backend
```
fastapi dev main.py
```

### `main.py`
> contains the POST method to send pdf and question to the backend, and returns the answer from the chatbot as an API response

**Embedding**
- extracting texts from the pdf context and splitting the texts into chunks
- embeds the question
- embeds the chunks of context

**Retrieval**
- doing a similarity search between the question embeddings and context embeddings
- sort and retrieve the top 5 chunks with the highest similarity score

**Generation**
- format a prompt to be passed into the chatbot
- chat with the chatbot

### `rag_chatbot.py`
> contains the logic of **Embedding**, **Retrieval** and **Generation**

### Models Used

**Embedding Model** :  *sentence-transformers/all-mpnet-base-v2*
```
model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}
hf = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
    )
```
**Large Language Model** : *tiiuae/falcon-7b-instruct*
```
huggingfacehub_api_token = "Your-Huggingface-API-token"
llm = HuggingFaceEndpoint(repo_id='tiiuae/falcon-7b-instruct', huggingfacehub_api_token=huggingfacehub_api_token)
```
### Functions

`extract_text_from_pdf`
- using the `fitz` library to open the pdf file
- returns the texts found in the file

`load_split`
- splits the texts into chunks using Langchain's `RecursiveCharacterTextSplitter`
- returns an array of chunks of texts

`embed_context`,  `embed_prompt`
- embeds the context and prompt and returns the embeddings

`similarity_search`
- running a similarity search using sklearn's `cosine_similarity` between the question embeddings and context embeddings
- returns a similarity matrix 

`chat_with_bot`
- feeds the input into the LLM and returns the response

## Frontend Set Up
```
cd frontend
npm install
npm run dev
```

*Things to consider*
- changing the models for more accurate results
- using a vector database to do a retrieval instead of cosine similarity
- prompt engineering