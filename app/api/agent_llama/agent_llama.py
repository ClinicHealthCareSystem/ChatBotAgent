from fastapi import APIRouter
from pydantic import BaseModel
from app.chatbot.agent_llama.tools_llama import agent_executor

router = APIRouter()  

class InputModel(BaseModel):
    input: str

@router.post("/agent_llama")
def response_agent_bot(data: InputModel):
    input_text = data.input
    response = agent_executor.invoke({"input": input_text, "chat_history":[]})
    return {"Resposta do agent": response}