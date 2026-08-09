from sqlalchemy import func, select
from sqlalchemy.orm import Session
from .models import Order

VALID_STATUSES = {"completed", "shipped"}


def base_revenue_query():
    return select(Order).where(Order.status.in_(VALID_STATUSES))


def summary(db: Session) -> dict:
    orders = db.scalar(select(func.count(Order.id)).where(Order.status.in_(VALID_STATUSES))) or 0
    revenue = db.scalar(
        select(func.coalesce(func.sum(Order.quantity * Order.unit_price), 0.0))
        .where(Order.status.in_(VALID_STATUSES))
    ) or 0.0
    customers = db.scalar(
        select(func.count(func.distinct(Order.customer_id)))
        .where(Order.status.in_(VALID_STATUSES))
    ) or 0
    aov = float(revenue) / orders if orders else 0.0
    return {
        "orders": int(orders),
        "customers": int(customers),
        "revenue": round(float(revenue), 2),
        "average_order_value": round(aov, 2),
    }


def category_performance(db: Session) -> list[dict]:
    stmt = (
        select(
            Order.category,
            func.sum(Order.quantity).label("units"),
            func.sum(Order.quantity * Order.unit_price).label("revenue"),
        )
        .where(Order.status.in_(VALID_STATUSES))
        .group_by(Order.category)
        .order_by(func.sum(Order.quantity * Order.unit_price).desc())
    )
    return [
        {"category": r.category, "units": int(r.units), "revenue": round(float(r.revenue), 2)}
        for r in db.execute(stmt).all()
    ]


def product_performance(db: Session) -> list[dict]:
    stmt = (
        select(
            Order.product,
            Order.category,
            func.sum(Order.quantity).label("units"),
            func.sum(Order.quantity * Order.unit_price).label("revenue"),
        )
        .where(Order.status.in_(VALID_STATUSES))
        .group_by(Order.product, Order.category)
        .order_by(func.sum(Order.quantity * Order.unit_price).desc())
    )
    return [
        {
            "product": r.product,
            "category": r.category,
            "units": int(r.units),
            "revenue": round(float(r.revenue), 2),
        }
        for r in db.execute(stmt).all()
    ]
