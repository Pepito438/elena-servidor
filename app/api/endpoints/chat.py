from fastapi import APIRouter
from pydantic import BaseModel
from app.core.elena import ask_elena

router = APIRouter()

class Message(BaseModel):
    prompt: str

@router.post("/")
async def chat_with_elena(message: Message):
    return {"response": ask_elena(message.prompt)}
