from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.deps import get_current_user
from app.services.generator import generator

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: list

@router.post("/", response_model=QueryResponse)
async def ask_question(
    query: QueryRequest,
    current_user=Depends(get_current_user)
):
    result = await generator.generate_answer(query.question)
    return result
