from fastapi import FastAPI
from pydantic import BaseModel
import os

# 🔑 CARGAR API KEY (ANTES DE TODO)
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

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

# 🧠 Embeddings (GRATIS LOCAL)
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 📚 Base de conocimiento
db = Chroma(persist_directory="./db", embedding_function=embedding)

# 🔥 Cargar datos solo si está vacío
try:
    if len(db.get()["documents"]) == 0:
        db.add_texts(data)
        db.persist()
except:
    db.add_texts(data)
    db.persist()

# 🧠 Memoria conversación
memory = ConversationBufferMemory()

# 🤖 IA (Gemini)
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

conversation = ConversationChain(
    llm=llm,
    memory=memory
)

# 📩 Modelo entrada
class Message(BaseModel):
    message: str

# 🔍 Buscar en conocimiento (más inteligente)
def buscar_respuesta(pregunta):
    try:
        docs = db.similarity_search_with_score(pregunta, k=1)

        if docs:
            doc, score = docs[0]

            # 🔥 Ajusta este valor si quieres más precisión
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

    # 🔥 1. Buscar en TU conocimiento
    respuesta = buscar_respuesta(pregunta)

    if respuesta:
        return {"reply": respuesta}

    # 🔥 2. IA con personalidad de vendedor
    prompt = f"""
    Eres un asesor tecnológico experto en ventas.

    Tu objetivo es:
    - entender al cliente
    - ofrecer soluciones
    - convencer sin ser agresivo

    Servicios:
    - ERP (Odoo)
    - desarrollo web
    - chatbots
    - automatización

    Responde corto, claro y profesional.

    Cliente: {pregunta}
    """

    try:
        # 👉 usar memoria
        response = conversation.predict(input=prompt)
        return {"reply": response}
    except:
        return {"reply": "Hubo un error con la IA"}
