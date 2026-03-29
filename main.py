from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

from langchain_google_genai import ChatGoogleGenerativeAI

app = FastAPI()

# 🔥 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm = ChatGoogleGenerativeAI(model="gemini-1.0-pro")

class Message(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "ok"}

@app.post("/chat")
async def chat(msg: Message):
    try:
        response = llm.invoke(msg.message)
        return {"reply": response.content}
    except Exception as e:
         return {"reply": str(e)}
