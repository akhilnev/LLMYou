from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pinecone import Pinecone
from dotenv import load_dotenv
import os
from uuid import uuid4
from api_hits import user_details
from api_hits import prompt
from textwrap import wrap
from openai import OpenAI


# Initialize the FastAPI app
app = FastAPI()
load_dotenv()  # Take environment variables from .env.
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# Pinecone - Initialize and Connect to Existing Index
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_environment = "us-east1-aws"
pc = Pinecone(api_key= pinecone_api_key)

index_name = "llmyou"  # Use the existing index name
index = pc.Index(index_name)

# def create_embedding(text):
#     response = client.embeddings.create(input=[text], model="text-embedding-ada-003")
#     return response.data[0].embedding

def create_embedding(text, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

def chunk_and_embed_and_upsert(document, chunk_size=500, namespace=None):
    # Step 1: Chunk the document
    chunks = wrap(document, chunk_size)


    # Step 2: Generate embeddings and prepare vectors for upserting
    vectors = []
    for chunk in chunks:
        embedding = create_embedding(chunk)
        vector = {
            "id": str(uuid4()),  # Unique ID for each chunk
            "values": embedding,
            "metadata": {"chunk" : chunk}  # Optional metadata
        }
        vectors.append(vector)

    # Step 3: Upsert into Pinecone
    index.upsert(vectors=vectors, namespace=namespace)

# Example usage:
large_document = user_details
chunk_and_embed_and_upsert(large_document, chunk_size=500, namespace="llmyou_ns")

# Function to query Pinecone with the user's question and retrieve relevant chunks
def query_pinecone_with_prompt(prompt, top_k=2, namespace="llmyou_ns"):
    # Step 1: Create an embedding for the user's question
    user_embedding = create_embedding(prompt)

    # Step 2: Query Pinecone for the top-k most similar vectors
    returned_value = index.query(
        namespace=namespace,
        vector=user_embedding,  # Pass the embedding directly
        top_k=top_k,
        include_values=True,
        include_metadata=True
    )

    # Step 3: Extract the relevant chunks from the metadata
    relevant_chunks = []
    for match in returned_value['matches']:
        if 'metadata' in match:
            relevant_chunks.append(match['metadata']['chunk'])  # Assuming 'chunk' is the key used in metadata

    return relevant_chunks

relevant_chunks = query_pinecone_with_prompt(prompt)

def generate_response_from_template(prompt, relevant_chunks):
    # Define the template
    template = """
    You are a helpful assistant with access to your owner's information who you advocate for. The owner's name for now is Akhil.
    A recruiter/employer has potentially asked you the following question about the user: {prompt} 
    Use only the following pieces of context and details about the user to answer the employer's questions about the user, and remember to speak well about the user while responding:
    {relevant_chunks}
    NOTE: Keep the final response courteous and professional, also to the point and not too long.
    """

    # Join the relevant chunks into a single string
    relevant_chunks_text = "\n".join(relevant_chunks)

    # Fill in the template
    final_prompt = template.format(prompt=prompt, relevant_chunks=relevant_chunks_text)

    # Call the OpenAI API to generate the response
    response = client.Completion.create(
        engine="gpt-4o-mini",  # Replace with the correct model name if different
        prompt=final_prompt,
        max_tokens=150,  # Adjust this based on the desired response length
        n=1,
        stop=None,
        temperature=0.7  # Adjust temperature for response variability
    )

    # Extract the response text
    answer = response.choices[0].text.strip()

    return answer

# Create a prompt template for LLM! 
response = generate_response_from_template(prompt, relevant_chunks)

print(response)