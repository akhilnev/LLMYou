from fastapi import FastAPI, HTTPException
from file_parser import parse_file_to_string, user_details
from main import generate_response_from_template, query_pinecone_with_prompt, classify_and_organize_user_info, create_tavus_conversation
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/generate_response")
async def generate_response(prompt: str):
    try:
        relevant_chunks = query_pinecone_with_prompt(prompt)
        response = generate_response_from_template(prompt, relevant_chunks)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/create_tavus_meeting")
async def create_tavus_meeting():
    try:
        organized_user_details = classify_and_organize_user_info(user_details)
        conversational_context = f"""
        You are a helpful assistant with access to your owner's information who you advocate for. The owner's name for now is Akhil.
        A recruiter/employer/fellow student has potentially asked you the following question about the user, and you need to help them understand more about Akhil and be adroit in your responses. Use only the following info which Akhil has provided about him:
        {organized_user_details} 
        """
        tavus_response = create_tavus_conversation(conversational_context)
        return {"meeting_link": tavus_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
