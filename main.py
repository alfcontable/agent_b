from fastapi import FastAPI
from pydantic import BaseModel
import os

# 🔑 API KEY
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

# Gemini
from langchain_google_genai import ChatGoogleGenerativeAI

# Chroma
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# Datos
from data import data

app = FastAPI()

# 🧠 Embeddings (ligero)
embedding = HuggingFaceEmbeddings()

# 📚 Base conocimiento
db = Chroma(embedding_function=embedding)

# 🔥 Cargar datos
db.add_texts(data)

# 🤖 Modelo IA
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# 📩 Entrada
class Message(BaseModel):
    message: str

# 🔍 Buscar en base
def buscar_respuesta(pregunta):
    try:
        docs = db.similarity_search_with_score(pregunta, k=1)

        if docs:
            doc, score = docs[0]

            if score < 0.5:
                return doc.page_content
    except:
        pass

    return None

@app.get("/")
def home():
    return {"status": "ok"}

@app.post("/chat")
async def chat(msg: Message):

    pregunta = msg.message

    # 🔥 1. Buscar en tus datos
    respuesta = buscar_respuesta(pregunta)

    if respuesta:
        return {"reply": respuesta}

    # 🔥 2. IA vendedor
    prompt = f"""
    Eres un asesor tecnológico experto en ventas.

    Servicios:
    - ERP (Odoo)
    - desarrollo web
    - chatbots
    - automatización

    Responde de forma clara, profesional y convincente.

    Cliente: {pregunta}
    """

    try:
        response = llm.invoke(prompt)
        return {"reply": response.content}
    except:
        return {"reply": "Error en IA"}
