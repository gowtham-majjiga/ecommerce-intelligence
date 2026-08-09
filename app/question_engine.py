from sqlalchemy.orm import Session
from .analytics import category_performance, product_performance, summary

INTENTS = {
    "category": ("category", "categories", "category revenue", "category performance"),
    "product": ("product", "products", "best selling", "top product"),
    "summary": ("overall", "total", "summary", "orders", "revenue", "customers", "average order"),
}


def detect_intent(question: str) -> str:
    q = question.lower()
    if any(term in q for term in INTENTS["category"]):
        return "category"
    if any(term in q for term in INTENTS["product"]):
        return "product"
    return "summary"


def answer_question(db: Session, question: str) -> dict:
    intent = detect_intent(question)

    if intent == "category":
        rows = category_performance(db)
        if not rows:
            raise ValueError("No completed or shipped orders are available.")
        top = rows[0]
        total = sum(r["revenue"] for r in rows)
        share = top["revenue"] / total if total else 0
        sql = "SELECT category, SUM(quantity) AS units, SUM(quantity * unit_price) AS revenue FROM orders WHERE status IN ('completed','shipped') GROUP BY category ORDER BY revenue DESC;"
        return {
            "answer": f"{top['category']} generates the highest revenue at ${top['revenue']:,.2f}.",
            "evidence": [
                {"metric": "top_category", "value": top["category"]},
                {"metric": "revenue", "value": top["revenue"]},
                {"metric": "revenue_share", "value": round(share, 3)},
            ],
            "sql_used": sql,
            "confidence": round(min(0.99, 0.75 + min(len(rows), 5) * 0.04), 2),
            "recommendation": f"Prioritize inventory and campaign analysis for {top['category']} while monitoring its revenue share.",
        }

    if intent == "product":
        rows = product_performance(db)
        if not rows:
            raise ValueError("No completed or shipped orders are available.")
        top = rows[0]
        sql = "SELECT product, category, SUM(quantity) AS units, SUM(quantity * unit_price) AS revenue FROM orders WHERE status IN ('completed','shipped') GROUP BY product, category ORDER BY revenue DESC;"
        return {
            "answer": f"{top['product']} is the top revenue-generating product at ${top['revenue']:,.2f}.",
            "evidence": [
                {"metric": "top_product", "value": top["product"]},
                {"metric": "category", "value": top["category"]},
                {"metric": "revenue", "value": top["revenue"]},
            ],
            "sql_used": sql,
            "confidence": 0.94,
            "recommendation": f"Review stock availability and conversion performance for {top['product']} before scaling promotion.",
        }

    data = summary(db)
    sql = "SELECT COUNT(*), COUNT(DISTINCT customer_id), SUM(quantity * unit_price) FROM orders WHERE status IN ('completed','shipped');"
    return {
        "answer": f"The dataset contains {data['orders']} completed/shipped orders generating ${data['revenue']:,.2f} in revenue.",
        "evidence": [
            {"metric": "orders", "value": data["orders"]},
            {"metric": "customers", "value": data["customers"]},
            {"metric": "revenue", "value": data["revenue"]},
            {"metric": "average_order_value", "value": data["average_order_value"]},
        ],
        "sql_used": sql,
        "confidence": 0.97,
        "recommendation": "Use category and product endpoints to identify where revenue concentration is strongest before making investment decisions.",
    }
