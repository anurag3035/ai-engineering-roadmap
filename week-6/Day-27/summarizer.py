from gemini_client import GeminiClient


class Summarizer:

    def __init__(self):

        self.client = GeminiClient()

    def summarize(self, messages):

        conversation = ""

        for message in messages:

            conversation += (
                f"{message['role']}: "
                f"{message['content']}\n"
            )

        prompt = f"""
Summarize the following conversation in less than 100 words.

Conversation:

{conversation}
"""

        summary = self.client.generate(prompt)

        return summary