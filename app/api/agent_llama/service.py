from fastapi import APIRouter
from app.schemas.agent_input_schemas import Message
from app.chatbot.agent_llama.tools_llama import llm

router = APIRouter()

@router.post("/fast_agent_llama")
async def chat_endpoint(data: Message):
    resposta = llm(data.message)
    return {"reply": resposta}