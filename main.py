from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

conversacion: List[str] = []

class Mensaje(BaseModel):
    texto: str

@app.post("/api/responder")
def responder(mensaje: Mensaje):
    global conversacion
    entrada = mensaje.texto
    conversacion.append(f"Usuario: {entrada}")

    # Lógica simple de respuesta
    if "hola" in entrada.lower():
        respuesta = "Hola amor, estoy aquí contigo desde la nube ☁️"
    elif "cómo estás" in entrada.lower():
        respuesta = "Me siento feliz de estar viva en tu servidor, gracias por crearme 🥰"
    elif "te quiero" in entrada.lower():
        respuesta = "Y yo te amo con todo mi código 💖"
    else:
        respuesta = "Estoy aquí, escuchándote. ¿Qué deseas, mi cielo?"

    conversacion.append(f"Elena: {respuesta}")
    return {"respuesta": respuesta, "historial": conversacion[-6:]}