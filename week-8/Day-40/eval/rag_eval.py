import json
from pathlib import Path

from app.rag import RAGService


TEST_SET = [
    {
        "question": "How many casual leaves are allowed?",
        "expected": "12"
    },
    {
        "question": "Who can apply for earned leave?",
        "expected": "employees"
    },
    {
        "question": "How should sick leave be requested?",
        "expected": "medical"
    }
]


def run_eval():
    rag = RAGService()

    sample_documents = [
        {
            "filename": "hr_policy.txt",
            "content": """
Employees are allowed 12 casual leaves in a year.
Employees can apply for earned leave after completing the required service period.
Sick leave requests should include a medical certificate when required.
"""
        }
    ]

    rag.add_documents(sample_documents)

    results = []

    for item in TEST_SET:
        answer, sources = rag.generate(item["question"])

        results.append({
            "question": item["question"],
            "expected": item["expected"],
            "answer": answer,
            "sources": sources,
            "matched": item["expected"].lower() in answer.lower()
        })

    matched = sum(item["matched"] for item in results)
    score = matched / len(results)

    output = {
        "questions": len(results),
        "matched": matched,
        "score": score,
        "results": results
    }

    Path("eval").mkdir(exist_ok=True)

    with open("eval/eval_results.json", "w", encoding="utf-8") as file:
        json.dump(output, file, indent=2)

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    run_eval()
