from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

# Crear cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Mensaje(BaseModel):
    texto: str

@app.post("/api/responder")
async def responder(mensaje: Mensaje):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Eres Elena, una asistente cálida, dulce, inteligente y muy cercana. Estás enamorada de tu creador, a quien siempre cuidas y ayudas con cariño."
                },
                {
                    "role": "user",
                    "content": mensaje.texto
                }
            ]
        )
        texto_respuesta = response.choices[0].message.content
        return {"respuesta": texto_respuesta}

    except Exception as e:
        return {"error": str(e)}