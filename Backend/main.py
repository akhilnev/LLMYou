from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pinecone import Pinecone
from dotenv import load_dotenv
import os
from uuid import uuid4
from api_hits import user_details
from textwrap import wrap
from openai import OpenAI

client = OpenAI()

# Initialize the FastAPI app
app = FastAPI()
load_dotenv()  # Take environment variables from .env.

# Pinecone - Initialize and Connect to Existing Index
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_environment = "us-east1-aws"
pc = Pinecone(api_key= pinecone_api_key )

index_name = "llmyou"  # Use the existing index name
index = pc.Index(index_name)

def create_embedding(text):
    response = client.embeddings.create(input=[text], model="text-embedding-ada-002")
    return response.data[0].embedding

def chunk_and_embed_and_upsert(document, chunk_size=500, namespace=None):
    # Step 1: Chunk the document
    chunks = wrap(document, chunk_size)

    # Step 2: Generate embeddings and prepare vectors for upserting
    vectors = []
    for chunk in enumerate(chunks):
        embedding = create_embedding(chunk)
        vector = {
            "id": str(uuid4()),  # Unique ID for each chunk
            "values": embedding,
            "metadata": {chunk}  # Optional metadata
        }
        vectors.append(vector)

    # Step 3: Upsert into Pinecone
    index.upsert(vectors=vectors, namespace=namespace)

# Example usage:
large_document = user_details
chunk_and_embed_and_upsert(large_document, chunk_size=500, namespace="llmyou_ns")

# Create a prompt template for LLM! 
template = """
You are a helpful assistant with access to the user's information. 
Use the following pieces of context and details about the user to answer people's questions about the user, and remember to praise the user while responding:
{context}
"""