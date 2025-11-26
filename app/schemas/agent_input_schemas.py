from pydantic import BaseModel

class InputModel(BaseModel):
    input: str

class Message(BaseModel):
    message: str
