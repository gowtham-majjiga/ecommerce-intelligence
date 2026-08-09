# E-Commerce Intelligence Assistant

An AI-ready analytics backend that turns business questions into evidence-backed e-commerce insights.

## What it does

The application provides a structured workflow for questions such as:

> Which product categories generate the most revenue, and what should we prioritize next?

Instead of returning an unsupported answer, the service produces:

- **Answer** — concise business conclusion
- **Evidence** — metrics used to support the conclusion
- **SQL Used** — the executable analytical query
- **Confidence** — deterministic confidence based on data coverage
- **Recommendation** — an actionable next step

## Architecture

```text
Client / Dashboard
       |
       v
   FastAPI API
       |
       +---- Question Parser
       |
       +---- Analytics Service
       |          |
       |          v
       |      SQLAlchemy
       |          |
       |          v
       |       Database
       |
       +---- Evidence Builder
       |
       +---- Recommendation Engine
       v
Structured Business Insight
```

## Features

- REST API with FastAPI
- SQLAlchemy persistence layer
- SQLite for zero-configuration local development
- PostgreSQL-compatible database design
- Seeded e-commerce dataset
- Revenue, orders, AOV, category, product, and customer analytics
- Natural-language question routing using deterministic intent matching
- SQL transparency
- Evidence and confidence scoring
- Recommendation generation
- Validation and structured errors
- Automated tests
- Docker support

## Example

`POST /api/v1/ask`

```json
{
  "question": "Which category generates the most revenue?"
}
```

Response:

```json
{
  "answer": "Electronics generated the highest revenue in the current dataset.",
  "evidence": [
    {"metric": "top_category", "value": "Electronics"},
    {"metric": "revenue", "value": 18450.0}
  ],
  "sql_used": "SELECT ...",
  "confidence": 0.94,
  "recommendation": "Prioritize inventory and campaign analysis for Electronics."
}
```

## API

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Service health |
| GET | `/api/v1/summary` | Overall business metrics |
| GET | `/api/v1/categories` | Category performance |
| GET | `/api/v1/products` | Product performance |
| POST | `/api/v1/ask` | Ask a business question |

## Run locally

```bash
python -m venv .venv

# Windows
.venv\\Scripts\\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
python scripts/seed.py
uvicorn app.main:app --reload
```

Open the API docs at `http://127.0.0.1:8000/docs`.

Run tests:

```bash
pytest -q
```

## Docker

```bash
docker build -t ecommerce-intelligence .
docker run -p 8000:8000 ecommerce-intelligence
```

## Project structure

```text
ecommerce-intelligence/
├── app/
│   ├── api.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── analytics.py
│   ├── question_engine.py
│   └── recommendations.py
├── scripts/
│   └── seed.py
├── tests/
│   └── test_api.py
├── docs/
│   └── architecture.md
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

## Engineering decisions

The question layer does not invent SQL from arbitrary text. It maps supported business intents to parameterized, tested analytical queries. This makes the output inspectable and safer while leaving a clear extension point for an LLM-based SQL planner.

The database layer is isolated from analytics logic, so the application can move from SQLite to PostgreSQL without changing the API contract.

## Status

Portfolio project demonstrating backend engineering, SQL analytics, API design, explainability, and AI-ready architecture.
