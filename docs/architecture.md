# Architecture

## Core flow

```text
HTTP Request
    |
    v
FastAPI Router
    |
    +---- Request Validation (Pydantic)
    |
    v
Question Engine
    |
    +---- Intent Detection
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
    +---- Confidence Assessment
    |
    +---- Recommendation
    v
Structured JSON Response
```

## Why the question engine is deterministic

The first version of the product should be inspectable. Supported business intents map to explicit SQL patterns rather than allowing arbitrary text to execute against the database. This reduces risk and makes the output reproducible.

## AI extension point

A future LLM planner can convert a natural-language question into a typed intermediate representation such as:

```json
{
  "intent": "category_revenue",
  "filters": [],
  "group_by": ["category"],
  "metric": "revenue",
  "sort": "desc",
  "limit": 5
}
```

The analytics layer can then validate that representation before executing a known-safe query template.

## Database portability

The application defaults to SQLite for a zero-configuration demo but uses SQLAlchemy throughout. Setting `DATABASE_URL` allows a PostgreSQL deployment without changing API consumers.
