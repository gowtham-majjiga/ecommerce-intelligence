import os

os.environ["DATABASE_URL"] = "sqlite:///./test_ecommerce.db"

from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, SessionLocal, engine
from app.models import Order

client = TestClient(app)


def setup_module():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    db.add_all([
        Order(order_date=__import__('datetime').datetime(2026, 1, 1), customer_id="C001", product="Headphones", category="Electronics", quantity=2, unit_price=100, status="completed"),
        Order(order_date=__import__('datetime').datetime(2026, 1, 2), customer_id="C002", product="Shoes", category="Sports", quantity=1, unit_price=80, status="shipped"),
    ])
    db.commit()
    db.close()


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_summary():
    response = client.get("/api/v1/summary")
    assert response.status_code == 200
    assert response.json()["orders"] == 2
    assert response.json()["revenue"] == 280.0


def test_question_contract():
    response = client.post("/api/v1/ask", json={"question": "Which category generates the most revenue?"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["answer"]
    assert payload["sql_used"]
    assert 0 <= payload["confidence"] <= 1
    assert payload["recommendation"]
