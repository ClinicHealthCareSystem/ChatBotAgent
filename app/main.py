from fastapi import FastAPI
from app.api import agent

app = FastAPI(title="API")

@app.get("/")
def read_root():
    return {"message": "Hello World"}

app.include_router(agent.router, prefix="/api/bot", tags=["Bot"])