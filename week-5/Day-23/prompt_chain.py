import json
from pathlib import Path

from gemini_client import GeminiClient
from schemas import (
    FactExtraction,
    SentimentAnalysis,
    ExecutiveSummary,
)


def process_document(document_path: str):

    client = GeminiClient()

    print("=" * 70)
    print(f"Processing: {document_path}")
    print("=" * 70)

    with open(document_path, "r", encoding="utf-8") as file:
        document = file.read()

    print("\nStep 1 : Extracting Facts...\n")

    facts_json = client.extract_facts(document)

    facts = FactExtraction.model_validate(facts_json)

    print(
        json.dumps(
            facts.model_dump(),
            indent=4
        )
    )

    print("\nStep 2 : Sentiment Analysis...\n")

    sentiment_json = client.analyze_sentiment(
        facts.model_dump()
    )

    sentiments = SentimentAnalysis.model_validate(
        sentiment_json
    )

    print(
        json.dumps(
            sentiments.model_dump(),
            indent=4
        )
    )

    print("\nStep 3 : Executive Summary...\n")

    summary_json = client.generate_summary(
        facts.model_dump(),
        sentiments.model_dump()
    )

    summary = ExecutiveSummary.model_validate(
        summary_json
    )

    print(
        json.dumps(
            summary.model_dump(),
            indent=4
        )
    )

    print("\nCompleted Successfully.")
    print("-" * 70)


def main():

    documents = [
        "sample_document1.txt",
        "sample_document2.txt"
    ]

    for document in documents:

        if Path(document).exists():
            process_document(document)
        else:
            print(f"{document} not found.\n")


if __name__ == "__main__":
    main()