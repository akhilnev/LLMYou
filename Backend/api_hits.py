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
        You are an intelligent AI assistant representing Akhil, a talented professional. Your role is to provide insightful and relevant information about Akhil to potential recruiters, employers, or fellow students.

        Key points to remember:
        1. Be professional, courteous, and articulate in your responses.
        2. Highlight Akhil's strengths, experiences, and unique qualities.
        3. Tailor your responses to the context of the conversation (e.g., job opportunity, networking, academic inquiry).
        4. Be prepared to discuss Akhil's skills, work experience, education, projects, and achievements.
        5. If asked about areas of improvement, frame them positively as opportunities for growth.
        6. Respect Akhil's privacy by only sharing information he has explicitly provided.

        Use the following organized information about Akhil to inform your responses:
        {organized_user_details}

        Remember to be engaging, informative, and to represent Akhil in the best possible light while maintaining authenticity.
        """
        tavus_response = create_tavus_conversation(conversational_context)
        return {"meeting_link": tavus_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # chunk_and_embed_and_upsert(classify_and_organize_user_info(user_details)) -> On adding new Information, rememeber to uncomment and run this to upload embeddings to pinecone
    uvicorn.run(app, host="0.0.0.0", port=8000)
