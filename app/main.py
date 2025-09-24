from fastapi import FastAPI
from app.api.agent_llama.agent_llama import router  

app = FastAPI(title="API")

@app.get("/")
def read_root():
    return {"message": "Hello World"}

app.include_router(router, prefix="/api/bot", tags=["Bot"])