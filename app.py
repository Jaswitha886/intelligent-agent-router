import asyncio
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from agents.intent_classifier import classify_intent
from router.query_router import route
from orchestrator.debate_controller import run_debate
from agents.moderator_agent import moderate
from config.llm_config import ollama_client
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],      # Allow all methods (POST, OPTIONS)
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

@app.post("/ask")
async def ask_question(request: QueryRequest):
    query = request.query

    try:
        intent = await classify_intent(query)
        mode = route(intent)

        if mode == "single":
            final = await moderate(query, "", "")
            return {
                "mode": "single",
                "final": final
            }
        else:
            debate_result = await run_debate(query)
            return {
                "mode": "debate",
                "pro": debate_result["pro"],
                "con": debate_result["con"],
                "evidence": debate_result["evidence"],
                "final": debate_result["final"]
            }
    except ConnectionError as e:
        if "Ollama" in str(e) or "connect" in str(e).lower():
            from fastapi import HTTPException
            raise HTTPException(status_code=503, detail="Could not connect to local Ollama service. Please make sure Ollama is running.")
        raise
    except Exception as e:
        from fastapi import HTTPException
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@app.on_event("shutdown")
async def shutdown_event():
    await ollama_client.close()


# Serve static files AFTER all API routes
frontend_path = os.path.join(os.path.dirname(__file__), "frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")
