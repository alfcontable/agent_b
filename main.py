from fastapi import FastAPI
from pydantic import BaseModel
import os

# 🔑 API KEY
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

from langchain_google_genai import ChatGoogleGenerativeAI

app = FastAPI()

# 🤖 IA
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# 📩 Entrada
class Message(BaseModel):
    message: str

# 🧠 RESPUESTAS BASE (TU NEGOCIO)
def responder_negocio(pregunta):

    pregunta = pregunta.lower()

    if "erp" in pregunta or "odoo" in pregunta:
        return "Ofrecemos implementación de ERP como Odoo para automatizar tu empresa."

    if "pagina" in pregunta or "web" in pregunta:
        return "Creamos páginas web modernas, rápidas y optimizadas para tu negocio."

    if "chatbot" in pregunta:
        return "Desarrollamos chatbots inteligentes como este para automatizar tu atención."

    if "precio" in pregunta:
        return "Ofrecemos soluciones personalizadas. ¿Qué tipo de sistema necesitas?"

    return None

@app.get("/")
def home():
    return {"status": "ok"}

@app.post("/chat")
async def chat(msg: Message):

    pregunta = msg.message

    # 🔥 1. Respuesta rápida (sin IA)
    respuesta = responder_negocio(pregunta)

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

    Responde claro, corto y profesional.

    Cliente: {pregunta}
    """

    try:
        response = llm.invoke(prompt)
        return {"reply": response.content}
    except:
        return {"reply": "Error en IA"}
