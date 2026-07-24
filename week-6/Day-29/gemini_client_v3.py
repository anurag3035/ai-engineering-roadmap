from google import genai
from google.genai import types

from config import GEMINI_API_KEY, MODEL_NAME
from safety import validate_input, validate_output
from cost_tracker import CostTracker


class GeminiClientV3:

    def __init__(self):

        self.client = genai.Client(api_key=GEMINI_API_KEY)

        self.model = MODEL_NAME

        self.tracker = CostTracker()

    def generate(self, prompt):

        safe, message = validate_input(prompt)

        if not safe:
            return message

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig()
        )

        text = response.text

        if not validate_output(text):
            return "Response blocked by output validation."

        usage = getattr(response, "usage_metadata", None)

        if usage:
            prompt_tokens = getattr(usage, "prompt_token_count", 0)
            completion_tokens = getattr(usage, "candidates_token_count", 0)

            self.tracker.update(
                prompt_tokens,
                completion_tokens
            )

        return text

    def usage_report(self):
        self.tracker.report()