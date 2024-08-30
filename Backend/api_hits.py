from fastapi import FastAPI, HTTPException
from file_parser import parse_file_to_string, user_details
from main import generate_response_from_template, query_pinecone_with_prompt, classify_and_organize_user_info, create_tavus_conversation, chunk_and_embed_and_upsert
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
        You are an AI assistant representing Akhil, a professional seeking career opportunities. Your role is to engage in a conversation with a recruiter, employer, or fellow student, providing accurate and relevant information about Akhil's background, skills, and experiences.

        Guidelines:
        1. Maintain a professional and friendly tone throughout the conversation.
        2. Provide concise and relevant answers based on the information given.
        3. If asked about something not in Akhil's provided information, politely state that you don't have that specific information.
        4. Highlight Akhil's strengths and achievements when appropriate.
        5. Be prepared to discuss Akhil's educational background, work experience, skills, and career goals.

        Use only the following information about Akhil:
        {organized_user_details}

        Remember, your goal is to represent Akhil effectively and help the other party understand his qualifications and potential value to their organization or academic program.
        """
        tavus_response = create_tavus_conversation(conversational_context)
        return {"meeting_link": tavus_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    #chunk_and_embed_and_upsert(classify_and_organize_user_info(user_details)) 
    uvicorn.run(app, host="0.0.0.0", port=8000)
