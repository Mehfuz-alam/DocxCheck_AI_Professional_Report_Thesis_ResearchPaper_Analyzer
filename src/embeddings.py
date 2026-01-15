import os
import streamlit as st
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
from pinecone.exceptions import NotFoundException

# --- STREAMLIT COMPATIBLE CONFIGURATION ---
# Use st.secrets instead of os.getenv or st.getenv
try:
    PINECONE_API_KEY = st.secrets["PINECONE_API_KEY"]
    PINECONE_ENV = st.secrets["PINECONE_ENV"]
    PINECONE_INDEX_NAME = st.secrets["PINECONE_INDEX"]
except KeyError as e:
    st.error(f"Missing Secret: {e}. Please add it to Streamlit Cloud Settings > Secrets.")
    st.stop()

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# Index Initialization logic
if PINECONE_INDEX_NAME not in [idx.name for idx in pc.list_indexes()]:
    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region=PINECONE_ENV)
    )

index = pc.Index(PINECONE_INDEX_NAME)

# Use st.cache_resource to load the model once and share it across user sessions
@st.cache_resource
def get_embed_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

embed_model = get_embed_model()

def create_embeddings(doc_folder):
    from src.document_parser import parse_document
    
    try:
        index.delete(delete_all=True) 
        print("Existing index cleared.")
    except NotFoundException:
        print("Index is already empty or namespace not found. Skipping clear.")
    except Exception as e:
        print(f"An unexpected error occurred during clearing: {e}")

    files_indexed = 0
    for file in os.listdir(doc_folder):
        if file.endswith((".pdf", ".docx")):
            path = os.path.join(doc_folder, file)
            text, _ = parse_document(path)
            
            vector = embed_model.encode([text])[0].tolist()
            index.upsert(vectors=[(file, vector, {"text": text})])
            files_indexed += 1
            
    return f"Embeddings refreshed for {files_indexed} file(s)."

def search_embeddings(query_text, top_k=3):
    query_vector = embed_model.encode([query_text])[0].tolist()
    res = index.query(vector=query_vector, top_k=top_k, include_metadata=True)
    return [match['metadata']['text'] for match in res['matches']]