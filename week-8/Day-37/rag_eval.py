import json
import os
from datetime import datetime

from datasets import Dataset
from dotenv import load_dotenv
from google import genai

from ragas import evaluate
from ragas.metrics import (
    Faithfulness,
    AnswerRelevancy,
    ContextPrecision,
    ContextRecall
)
from ragas.llms import llm_factory
from ragas.embeddings import GoogleEmbeddings


load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "gemini-2.5-flash-lite"
)

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not set")


client = genai.Client(
    api_key=API_KEY
)


llm = llm_factory(
    MODEL_NAME,
    provider="google",
    client=client
)


embeddings = GoogleEmbeddings(
    client=client,
    model="gemini-embedding-001"
)


eval_data = [
    {
        "question": "How many casual leaves are allowed?",
        "answer": "Employees are allowed 12 casual leaves per year.",
        "contexts": [
            "Employees are entitled to 12 casual leaves in a calendar year."
        ],
        "ground_truth": "Employees are allowed 12 casual leaves per year."
    },
    {
        "question": "How many sick leaves are allowed?",
        "answer": "Employees are allowed 10 sick leaves per year.",
        "contexts": [
            "Employees can take up to 10 sick leaves during a calendar year."
        ],
        "ground_truth": "Employees are allowed 10 sick leaves per year."
    },
    {
        "question": "How many working hours are required per day?",
        "answer": "Employees are expected to work 8 hours per day.",
        "contexts": [
            "The standard working schedule consists of 8 working hours per day."
        ],
        "ground_truth": "Employees are expected to work 8 hours per day."
    },
    {
        "question": "What is the standard notice period?",
        "answer": "The standard notice period is 30 days.",
        "contexts": [
            "Employees are required to provide a 30-day notice period before resignation."
        ],
        "ground_truth": "The standard notice period is 30 days."
    },
    {
        "question": "Is remote work allowed?",
        "answer": "Remote work is allowed with manager approval.",
        "contexts": [
            "Employees may work remotely after receiving approval from their reporting manager."
        ],
        "ground_truth": "Remote work is allowed with manager approval."
    },
    {
        "question": "When is the salary paid?",
        "answer": "Salary is paid on the last working day of each month.",
        "contexts": [
            "Monthly salaries are processed on the last working day of every month."
        ],
        "ground_truth": "Salary is paid on the last working day of each month."
    },
    {
        "question": "How should employees apply for leave?",
        "answer": "Employees should apply through the company leave portal.",
        "contexts": [
            "All leave requests must be submitted through the official employee leave portal."
        ],
        "ground_truth": "Employees should apply through the company leave portal."
    },
    {
        "question": "Who approves employee leave?",
        "answer": "The reporting manager approves employee leave requests.",
        "contexts": [
            "Leave requests are reviewed and approved by the employee's reporting manager."
        ],
        "ground_truth": "The reporting manager approves employee leave requests."
    },
    {
        "question": "Are public holidays included in annual leave?",
        "answer": "Public holidays are not counted as annual leave.",
        "contexts": [
            "Official public holidays are separate from annual leave and are not deducted from an employee's leave balance."
        ],
        "ground_truth": "Public holidays are not counted as annual leave."
    },
    {
        "question": "Can unused casual leave be carried forward?",
        "answer": "Unused casual leave cannot be carried forward.",
        "contexts": [
            "Casual leave must be used within the calendar year and cannot be carried forward."
        ],
        "ground_truth": "Unused casual leave cannot be carried forward."
    },
    {
        "question": "What happens during the probation period?",
        "answer": "Employees remain under probation for six months.",
        "contexts": [
            "New employees normally complete a six-month probation period."
        ],
        "ground_truth": "Employees remain under probation for six months."
    },
    {
        "question": "Can employees work overtime?",
        "answer": "Overtime requires prior manager approval.",
        "contexts": [
            "Employees must obtain prior approval from their manager before working overtime."
        ],
        "ground_truth": "Overtime requires prior manager approval."
    },
    {
        "question": "How should employees report an absence?",
        "answer": "Employees should inform their manager as soon as possible.",
        "contexts": [
            "Employees who cannot attend work should notify their reporting manager as soon as reasonably possible."
        ],
        "ground_truth": "Employees should inform their manager as soon as possible."
    },
    {
        "question": "Is an identity card required inside the office?",
        "answer": "Employees must carry their company identity card inside the office.",
        "contexts": [
            "Employees are required to carry and display their company identity card while on office premises."
        ],
        "ground_truth": "Employees must carry their company identity card inside the office."
    },
    {
        "question": "Who should employees contact for HR-related issues?",
        "answer": "Employees should contact the HR department.",
        "contexts": [
            "Employees should contact the Human Resources department for HR-related questions and concerns."
        ],
        "ground_truth": "Employees should contact the HR department."
    }
]


def run_evaluation():

    dataset = Dataset.from_list(eval_data)

    metrics = [
        Faithfulness(llm=llm),
        AnswerRelevancy(
            llm=llm,
            embeddings=embeddings
        ),
        ContextPrecision(llm=llm),
        ContextRecall(llm=llm)
    ]

    print("Running RAG evaluation...")
    print("Number of questions:", len(eval_data))

    result = evaluate(
        dataset,
        metrics=metrics
    )

    print("\nEvaluation completed.")
    print(result)

    results_dict = result.to_pandas().to_dict(
        orient="records"
    )

    for index, item in enumerate(results_dict):
        item["question"] = eval_data[index]["question"]

    metric_names = [
        "faithfulness",
        "answer_relevancy",
        "context_precision",
        "context_recall"
    ]

    mean_scores = {}

    for metric in metric_names:

        values = []

        for item in results_dict:

            value = item.get(metric)

            if value is not None:
                values.append(float(value))

        if values:
            mean_scores[metric] = sum(values) / len(values)

    ranked_questions = []

    for item in results_dict:

        scores = []

        for metric in metric_names:

            value = item.get(metric)

            if value is not None:
                scores.append(float(value))

        if scores:

            average_score = sum(scores) / len(scores)

            ranked_questions.append(
                {
                    "question": item["question"],
                    "average_score": average_score
                }
            )

    ranked_questions.sort(
        key=lambda x: x["average_score"]
    )

    worst_questions = ranked_questions[:3]

    final_results = {
        "timestamp": datetime.now().isoformat(),
        "total_questions": len(eval_data),
        "mean_scores": mean_scores,
        "worst_3_questions": worst_questions,
        "question_results": results_dict
    }

    os.makedirs(
        "eval_history",
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    output_file = (
        f"eval_history/rag_eval_results_{timestamp}.json"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            final_results,
            file,
            indent=4
        )

    print("\nMean Scores:")

    for metric, score in mean_scores.items():

        print(
            f"{metric}: {score:.3f}"
        )

    print("\n3 Worst Performing Questions:")

    for item in worst_questions:

        print(
            f"- {item['question']}"
        )

        print(
            f"  Score: {item['average_score']:.3f}"
        )

    print(
        f"\nResults saved to: {output_file}"
    )


if __name__ == "__main__":
    run_evaluation()