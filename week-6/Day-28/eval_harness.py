import json

from gemini_client import GeminiClient
from judge import Judge


client = GeminiClient()
judge = Judge()


with open(
    "questions.json",
    "r",
    encoding="utf-8"
) as file:

    questions = json.load(file)


results = []

for item in questions:

    question = item["question"]
    reference = item["reference"]

    answer = client.generate(question)

    evaluation = judge.evaluate(
        question,
        answer,
        reference
    )

    results.append(
        {
            "question": question,
            "generated_answer": answer,
            "evaluation": evaluation
        }
    )

    print("=" * 60)
    print("Question:", question)
    print()
    print("Answer:")
    print(answer)
    print()
    print("Evaluation:")
    print(evaluation)
    print("=" * 60)


with open(
    "eval_results.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        results,
        file,
        indent=4,
        ensure_ascii=False
    )

print("\nEvaluation completed.")