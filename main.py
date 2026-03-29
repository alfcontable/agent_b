from fastapi import FastAPI
from pydantic import BaseModel
import os

# LangChain
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# Gemini
from langchain_google_genai import ChatGoogleGenerativeAI

# Datos
from data import data

app = FastAPI()

# 🔑 API KEY
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

# 🧠 Embeddings (GRATIS LOCAL)
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 📚 Base de conocimiento
db = Chroma(persist_directory="./db", embedding_function=embedding)

# 👉 Cargar datos (solo primera vez)
if not db.get()["documents"]:
    db.add_texts(data)

# 🧠 Memoria conversación
memory = ConversationBufferMemory()

# 🤖 IA (fallback)
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

conversation = ConversationChain(llm=llm, memory=memory)

# 📩 Modelo entrada
class Message(BaseModel):
    message: str

# 🔍 Buscar en conocimiento
def buscar_respuesta(pregunta):
    docs = db.similarity_search(pregunta, k=1)
    if docs:
        return docs[0].page_content
    return None

@app.get("/")
def home():
    return {"status": "ok"}

@app.post("/chat")
async def chat(msg: Message):

    pregunta = msg.message

    # 🔥 1. Buscar en TU conocimiento
    respuesta = buscar_respuesta(pregunta)

    if respuesta:
        return {"reply": respuesta}

    # 🔥 2. IA con personalidad (VENDEDOR)
    prompt = f"""
    Eres un asistente vendedor experto en tecnología.
    Vendes servicios como:
    - ERP (Odoo)
    - Desarrollo web
    - Chatbots
    - Automatización

    Responde de forma profesional y convincente.

    Cliente: {pregunta}
    """

    try:
        response = llm.invoke(prompt)
        return {"reply": response.content}
    except:
        return {"reply": "Error en IA"}