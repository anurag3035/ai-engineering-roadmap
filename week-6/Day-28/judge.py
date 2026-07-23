from gemini_client import GeminiClient


class Judge:

    def __init__(self):

        self.client = GeminiClient()

    def evaluate(self, question, answer, reference):

        prompt = f"""
You are an AI evaluator.

Question:
{question}

Generated Answer:
{answer}

Reference Answer:
{reference}

Give your evaluation in this format only.

Score: <1-5>

Reason:
<one short paragraph>
"""

        result = self.client.generate(prompt)

        return result