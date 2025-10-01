from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware



from agent_llama import responseLLM

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8081/"],
    allow_credentials=True,
    allow_methos=["POST"],
    allow_headers=[""],
)

class Message(BaseException):
    message: str

@app.post("/")
async def chat_endpoiny(data: Message):
    resposta = responseLLM(data.message)
    return {"reply": resposta}