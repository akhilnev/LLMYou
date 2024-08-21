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
import requests

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
    NOTE: Keep the final response courteous and professional, also to the point and not too long, and dont always start with the same thing, be creative and vary your responses.
    """

    # Join the relevant chunks into a single string
    relevant_chunks_text = "\n".join(relevant_chunks)

    # Fill in the template
    final_prompt = template.format(prompt=prompt, relevant_chunks=relevant_chunks_text)

    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": final_prompt },
        {"role": "user", "content": prompt}
    ]
    )
    # Extract the response text
    answer = response.choices[0].message.content.strip()

    return answer

# Create a prompt template for LLM! 
response = generate_response_from_template(prompt, relevant_chunks)

print(response)

def classify_and_organize_user_info(user_info_text):
    # Step 1: Use GPT-4o-mini to classify and organize the information
    classification_prompt = f"""
    You are an AI assistant. Please classify and organize the following user information into relevant categories like 'Work Experience', 'Skills', 'Education', 'Projects', etc. 
    Also, summarize key points under each category:
    
    {user_info_text}
    """
    
    # Call the GPT-4o-mini model to classify and organize the text
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": classification_prompt },
    ]
    )
    
    # Extract the organized text from the response
    organized_info = response.choices[0].message.content.strip()
    
    return organized_info

#! CONVERSATION AREA - WORKS :) BUT NEED TO REPLACE PERSONA ONCE MODEL IS TRAINED!  !#


user_details = classify_and_organize_user_info(user_details)

conversational_context = f"""
    You are a helpful assistant with access to your owner's information who you advocate for. The owner's name for now is Akhil.
    A recruiter/employer/fellow student has potentially asked you the following question about the user, and you need to help them udnerstand more about Akhil and be adroit in your responses. Use only the following info which Akhil has provided about him
    {user_details} 
    """

print(conversational_context)


# Ended up making the request online through the webhook on the Tavus Website ( Bought Premium for access to 3 replicas)
response_tavus = {"status":"training","replica_id":"r4f192f462"}

# Creating a conversation with the Tavus API

conversation_url_api = "https://tavusapi.com/v2/conversations"

payload = {
    "replica_id": "r79e1c033f",
    "persona_id": "p5317866",
    "conversation_name": "Getting User Information ",
    "conversational_context": conversational_context,
    "custom_greeting": "Hi, I am Akhil's AI. I would love to help you learn more about him!",
    "properties": {
        "max_call_duration": 120,
        "participant_left_timeout": 5
    }
}
headers = {
    "x-api-key": os.getenv("TAVUS_API_KEY"),
    "Content-Type": "application/json"
}

response = requests.request("POST", conversation_url_api, json=payload, headers=headers)

print(f"Join the link to the meeting here: {response.text}")