from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .analytics import category_performance, product_performance, summary
from .database import get_db
from .question_engine import answer_question
from .schemas import InsightResponse, QuestionRequest, SummaryResponse

router = APIRouter(prefix="/api/v1")

@router.get("/summary", response_model=SummaryResponse)
def get_summary(db: Session = Depends(get_db)):
    return summary(db)

@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    return {"data": category_performance(db)}

@router.get("/products")
def get_products(db: Session = Depends(get_db)):
    return {"data": product_performance(db)}

@router.post("/ask", response_model=InsightResponse)
def ask(request: QuestionRequest, db: Session = Depends(get_db)):
    try:
        return answer_question(db, request.question)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
