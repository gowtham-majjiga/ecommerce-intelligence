from pydantic import BaseModel, Field

class QuestionRequest(BaseModel):
    question: str = Field(min_length=5, max_length=500)

class Evidence(BaseModel):
    metric: str
    value: str | float | int

class InsightResponse(BaseModel):
    answer: str
    evidence: list[Evidence]
    sql_used: str
    confidence: float = Field(ge=0, le=1)
    recommendation: str

class SummaryResponse(BaseModel):
    orders: int
    customers: int
    revenue: float
    average_order_value: float
