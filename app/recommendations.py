def recommendation_for_category(category: str) -> str:
    return f"Prioritize {category} for inventory and campaign analysis, then validate the decision against margin and conversion data."


def confidence_from_coverage(rows: int, minimum: int = 3) -> float:
    if rows <= 0:
        return 0.0
    return round(min(0.99, 0.78 + 0.05 * min(rows / minimum, 3)), 2)
