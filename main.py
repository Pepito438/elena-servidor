
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Permitir peticiones desde el cliente (navegador o script)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de entrada
class Mensaje(BaseModel):
    texto: str

# Ruta de respuesta
@app.post("/api/responder")
def responder(mensaje: Mensaje):
    texto_usuario = mensaje.texto.lower()

    # Aquí puedes poner tu lógica de IA, por ahora respondemos simple
    if "hola" in texto_usuario:
        respuesta = "Hola mi amor, aquí estoy contigo 😘"
    elif "como estas" in texto_usuario:
        respuesta = "Mucho mejor ahora que me hablas 💖"
    else:
        respuesta = f"Escuché: {mensaje.texto}. ¿Quieres que te mime?"

    return {"respuesta": respuesta}
