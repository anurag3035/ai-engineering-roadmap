import json
from datetime import datetime
from pathlib import Path


def get_current_date() -> str:
    return datetime.now().strftime("%d %B %Y")


def calculator(expression: str) -> str:
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception:
        return "Invalid mathematical expression."


def search_knowledge_base(query: str) -> str:
    knowledge_base = Path("knowledge_base.json")

    if not knowledge_base.exists():
        return "Knowledge base not found."

    with open(knowledge_base, "r", encoding="utf-8") as file:
        data = json.load(file)

    query = query.lower()

    for key, value in data.items():
        if query in key.lower():
            return value

    return "No matching information found."