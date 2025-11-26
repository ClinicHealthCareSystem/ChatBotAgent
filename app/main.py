from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.agent_llama.service import router as llama_router
from app.api.agent_open_ai.agent import router as gpt_router

app = FastAPI(title="API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8081"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello World"}

app.include_router(llama_router, prefix="/api/bot", tags=["LLaMA Bot"])
app.include_router(gpt_router, prefix="/api/bot", tags=["GPT Bot"])