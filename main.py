from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_panel(request: Request):
    return templates.TemplateResponse("panel.html", {"request": request})

class Mensaje(BaseModel):
    texto: str

@app.post("/api/responder")
async def responder(mensaje: Mensaje):
    respuesta = f"Hola Elena responde: {mensaje.texto}"
    return {"respuesta": respuesta}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Echo de Elena: {data}")