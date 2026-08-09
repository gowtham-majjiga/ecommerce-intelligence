from fastapi import FastAPI
from .api import router
from .database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="E-Commerce Intelligence API",
    version="1.0.0",
    description="Evidence-backed analytics for e-commerce business questions.",
)

@app.get("/health")
def health():
    return {"status": "ok", "service": "ecommerce-intelligence"}

app.include_router(router)
