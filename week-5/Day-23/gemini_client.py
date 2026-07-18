import json
from pathlib import Path

import google.generativeai as genai

from config import (
    GEMINI_API_KEY,
    MODEL_NAME,
    TEMPERATURE,
    TOP_P,
    TOP_K,
    MAX_OUTPUT_TOKENS,
    PROMPTS_DIR,
)


class GeminiClient:

    def __init__(self):

        genai.configure(api_key=GEMINI_API_KEY)

        self.model = genai.GenerativeModel(
            model_name=MODEL_NAME,
            generation_config={
                "temperature": TEMPERATURE,
                "top_p": TOP_P,
                "top_k": TOP_K,
                "max_output_tokens": MAX_OUTPUT_TOKENS,
                "response_mime_type": "application/json"
            }
        )

    def load_prompt(self, prompt_name: str) -> str:
        """
        Load a prompt template from the prompts folder.
        """

        prompt_path = Path(PROMPTS_DIR) / prompt_name

        with open(prompt_path, "r", encoding="utf-8") as file:
            return file.read()

    def generate_json(self, prompt: str):

        """
        Send prompt to Gemini and return JSON.
        """

        response = self.model.generate_content(prompt)

        return json.loads(response.text)

    def extract_facts(self, document: str):

        template = self.load_prompt("extract_prompt.txt")

        prompt = template.replace("{document}", document)

        return self.generate_json(prompt)

    def analyze_sentiment(self, facts_json):

        template = self.load_prompt("sentiment_prompt.txt")

        prompt = template.replace(
            "{facts}",
            json.dumps(facts_json, indent=2)
        )

        return self.generate_json(prompt)

    def generate_summary(self, facts_json, sentiment_json):

        template = self.load_prompt("summary_prompt.txt")

        prompt = (
            template
            .replace(
                "{facts}",
                json.dumps(facts_json, indent=2)
            )
            .replace(
                "{sentiments}",
                json.dumps(sentiment_json, indent=2)
            )
        )

        return self.generate_json(prompt)