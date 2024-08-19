from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
import pinecone
import os 

#intialize the FastAPI app -> push to api_hits ? 
app = FastAPI()


# Pinecone - Vector Store
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=pinecone_api_key)
index_name = "llmyou"

# Initialize OpenAI - Embedding + LLM Usage 
openai_api_key = os.getenv("OPENAI_API_KEY")
llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

# Initialize vector store
vector_store = Pinecone.from_existing_index(index_name, embeddings)

# Create a prompt template
template = """
You are a helpful assistant with access to the user's information. 
Use the following pieces of context to answer the user's question:
{context}
"""