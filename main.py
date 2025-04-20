
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Mensaje(BaseModel):
    texto: str

BASE = "servidor/local/"
MEMORIA_PATH = BASE + "memoria.json"
FRASES_PATH = BASE + "frases.json"
PENDIENTES_PATH = BASE + "pendientes.json"

def cargar(path, tipo):
    if not os.path.exists(path):
        return {} if tipo == "dict" else []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {} if tipo == "dict" else []

def guardar(path, contenido):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(contenido, f, indent=2, ensure_ascii=False)

def detectar_intencion(texto, frases):
    texto_l = texto.lower()
    if any(p in texto_l for p in ["hola", "buenas", "hey", "ey"]):
        return "saludo"
    elif any(p in texto_l for p in ["quién eres", "cómo te llamas", "tu nombre"]):
        return "identidad"
    elif any(p in texto_l for p in ["estás ahí", "me oyes", "ei tú", "dónde estabas"]):
        return "presencia"
    elif any(p in texto_l for p in ["te quiero", "me gustas", "te amo"]):
        return "afecto"
    elif any(p in texto_l for p in ["sabes una cosa", "te cuento", "te digo algo"]):
        return "curiosidad"
    return "default"

@app.post("/api/responder")
def responder(mensaje: Mensaje):
    texto = mensaje.texto
    frases = cargar(FRASES_PATH, "dict")
    memoria = cargar(MEMORIA_PATH, "list")
    pendientes = cargar(PENDIENTES_PATH, "list")

    intencion = detectar_intencion(texto, frases)

    if intencion in frases and frases[intencion]:
        respuesta = random.choice(frases[intencion])
    else:
        respuesta = random.choice(frases["default"]).replace("{texto}", texto)
        if texto not in pendientes:
            pendientes.append(texto)
            guardar(PENDIENTES_PATH, pendientes)

    memoria.append({"usuario": texto, "elena": respuesta})
    guardar(MEMORIA_PATH, memoria)

    return {"respuesta": respuesta}
