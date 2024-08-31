from fastapi import FastAPI
from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone
from uuid import uuid4
from textwrap import wrap
import os
import requests
from testing import prompt
from file_parser import user_details
import json

# Initialize FastAPI app and load environment variables
app = FastAPI()
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("llmyou")

def create_embedding(text, model="text-embedding-3-small"):
    return client.embeddings.create(input=[text.replace("\n", " ")], model=model).data[0].embedding

def chunk_and_embed_and_upsert(document, chunk_size=100, namespace="llmyou_ns"):
    chunks = wrap(document, chunk_size)
    vectors = [
        {
            "id": str(uuid4()),
            "values": create_embedding(chunk),
            "metadata": {"chunk": chunk}
        }
        for chunk in chunks
    ]
    index.upsert(vectors=vectors, namespace=namespace)

def query_pinecone_with_prompt(prompt, top_k=2, namespace="llmyou_ns"):
    user_embedding = create_embedding(prompt)
    results = index.query(
        namespace=namespace,
        vector=user_embedding,
        top_k=top_k,
        include_metadata=True
    )
    return [match['metadata']['chunk'] for match in results['matches'] if 'metadata' in match]

def generate_response_from_template(prompt, relevant_chunks):
    template = """
    You are a helpful assistant with access to your owner's information who you advocate for. The owner's name for now is Akhil.
    A recruiter/employer has potentially asked you the following question about the user: {prompt} 
    Use only the following pieces of context and details about the user to answer the employer's questions about the user, and remember to speak well about the user while responding:
    {relevant_chunks}
    NOTE: Keep the final response courteous and professional, also to the point and not too long, and dont always start with the same thing, be creative and vary your responses.
    """
    final_prompt = template.format(prompt=prompt, relevant_chunks="\n".join(relevant_chunks))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": final_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def classify_and_organize_user_info(user_info_text):
    classification_prompt = f"""
    You are an AI assistant tasked with organizing and structuring user information. Please analyze the following user information and break it down into the most detailed and well-organized format possible. Follow these guidelines:

    1. Identify and create main categories such as 'Work Experience', 'Skills', 'Education', 'Projects', 'Achievements', 'Certifications', etc.
    2. Under each main category, create subcategories as needed. For example, under 'Skills', you might have 'Technical Skills', 'Soft Skills', 'Languages', etc.
    3. For each item of information, provide as much detail as possible, including dates, locations, specific responsibilities, technologies used, etc.
    4. Use bullet points or numbered lists to present information clearly and concisely.
    5. If there are any notable achievements or key highlights, emphasize them.
    6. Ensure that the information is presented in a logical and chronological order where applicable.
    7. If there are any gaps or inconsistencies in the information provided, note them for further clarification.

    Here's the user information to organize:

    {user_info_text}

    Please provide a comprehensive and well-structured breakdown of this information.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": classification_prompt}]
    )
    return response.choices[0].message.content.strip()

def create_tavus_conversation(conversational_context):
    payload = {
        "replica_id": "r79e1c033f",
        "persona_id": "p9a95912",
        "conversation_name": "Getting User Information",
        "conversational_context": conversational_context,
        "custom_greeting": "Hi, I am Akhil's AI. I would love to help you learn more about him!",
        "properties": {
            "max_call_duration": 180,
            "participant_left_timeout": 5
        }
    }
    headers = {
        "x-api-key": os.getenv("TAVUS_API_KEY"),
        "Content-Type": "application/json"
    }
    response = requests.post("https://tavusapi.com/v2/conversations", json=payload, headers=headers)
    response_data = json.loads(response.text)
    print(response_data)
    return response_data.get("conversation_url", "No URL found")

# Main execution
if __name__ == "__main__":
    # Process and upsert user details
    chunk_and_embed_and_upsert(classify_and_organize_user_info(user_details))

    # Generate response based on prompt
    relevant_chunks = query_pinecone_with_prompt(prompt)
    response = generate_response_from_template(prompt, relevant_chunks)
    print(response)

    # Classify and organize user info
    organized_user_details = classify_and_organize_user_info(user_details)
    
    # Create Tavus conversation
    conversational_context = f"""
    You are a helpful assistant with access to your owner's information who you advocate for. The owner's name for now is Akhil.
    A recruiter/employer/fellow student has potentially asked you the following question about the user, and you need to help them understand more about Akhil and be adroit in your responses. Use only the following info which Akhil has provided about him:
    {organized_user_details} 
    """
    tavus_response = create_tavus_conversation(conversational_context)
    print(f"Join the link to the meeting here: {tavus_response}")