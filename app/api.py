from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.database.vector_store import VectorStore
from app.services.synthesizer import Synthesizer

app = FastAPI(title="Customer Support RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str
    provider: str = "openai"
    filters: Optional[Dict[str, Any]] = Field(default="null", description="Optional metadata filters for the vector search")


vec = VectorStore()


@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        results = vec.search(
            query_text=request.question,
            limit=3,
            metadata_filter=request.filters,
            return_dataframe=False,
        )
        print(f"Raw vecs results: {results}")

        response = Synthesizer.generate_response(
            question=request.question,
            context=results,
            provider=request.provider,
        )
        return {
            "question": request.question,
            "answer": response.answer,
            "thoughts": response.thought_process,
            "enough_context": response.enough_context,
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
