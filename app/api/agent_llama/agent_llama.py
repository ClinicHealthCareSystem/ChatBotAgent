from fastapi import APIRouter
from app.chatbot.agent_llama.tools_llama import responseLLM
from app.schemas.agent_input_schemas import InputModel

router = APIRouter()


@router.post("/agent_llama")
def response_agent_bot(data: InputModel):
    input_text = data.input
    response = responseLLM(input_text)
    return {"Resposta do agent": response}
