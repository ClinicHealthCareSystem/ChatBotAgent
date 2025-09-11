from fastapi import APIRouter
from app.chatbot.tools import agent_executor
from app.schemas.agent_input_schemas import InputModel

router = APIRouter()


@router.post("/agent")
def response_agent_bot(data: InputModel):
    input = data.input
    response = agent_executor.invoke({"input": input})
    return {"Resposta do agent": response}
