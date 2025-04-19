from fastapi import FastAPI, Request
from pydantic import BaseModel
import os
import json

app = FastAPI()

CLAVE_SECRETA = os.getenv("CLAVE_ELENA", "1234")
MEMORIA_SYNC = "memoria_sincronizada.json"

class SincronizarMensaje(BaseModel):
    clave: str
    entrada: str
    respuesta: str

@app.post("/sincronizar/mensaje")
async def sincronizar_mensaje(datos: SincronizarMensaje):
    if datos.clave != CLAVE_SECRETA:
        return {"error": "clave inválida"}
    historial = []
    if os.path.exists(MEMORIA_SYNC):
        with open(MEMORIA_SYNC, "r", encoding="utf-8") as f:
            historial = json.load(f)
    historial.append({"user": datos.entrada, "elena": datos.respuesta})
    with open(MEMORIA_SYNC, "w", encoding="utf-8") as f:
        json.dump(historial[-50:], f, ensure_ascii=False, indent=2)
    return {"status": "ok"}

@app.get("/sincronizar/recuperar")
async def recuperar_historial(request: Request):
    clave = request.query_params.get("clave")
    if clave != CLAVE_SECRETA:
        return {"error": "clave inválida"}
    if os.path.exists(MEMORIA_SYNC):
        with open(MEMORIA_SYNC, "r", encoding="utf-8") as f:
            historial = json.load(f)
        return {"historial": historial}
    return {"historial": []}