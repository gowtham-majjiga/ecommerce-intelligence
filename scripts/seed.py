from datetime import datetime, timedelta
from pathlib import Path
import random
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.database import Base, SessionLocal, engine
from app.models import Order

Base.metadata.create_all(bind=engine)

random.seed(42)
products = [
    ("Wireless Headphones", "Electronics", 120.0),
    ("Mechanical Keyboard", "Electronics", 95.0),
    ("Running Shoes", "Sports", 80.0),
    ("Yoga Mat", "Sports", 35.0),
    ("Coffee Maker", "Home", 75.0),
    ("Desk Lamp", "Home", 42.0),
    ("Backpack", "Fashion", 55.0),
    ("Hoodie", "Fashion", 60.0),
]


def seed():
    db = SessionLocal()
    try:
        db.query(Order).delete()
        start = datetime(2026, 1, 1)
        rows = []
        for i in range(1, 101):
            product, category, price = random.choice(products)
            rows.append(Order(
                order_date=start + timedelta(days=random.randint(0, 90)),
                customer_id=f"C{random.randint(1, 35):03d}",
                product=product,
                category=category,
                quantity=random.randint(1, 4),
                unit_price=price,
                status=random.choices(["completed", "shipped", "cancelled"], weights=[55, 35, 10])[0],
            ))
        db.add_all(rows)
        db.commit()
        print(f"Seeded {len(rows)} orders")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
