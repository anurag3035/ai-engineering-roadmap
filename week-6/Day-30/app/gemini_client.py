from google import genai

from app.config import (
    GEMINI_API_KEY,
    MODEL_NAME
)


class GeminiClient:

    def __init__(self):

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        self.model = MODEL_NAME

    def generate(self, prompt):

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        return response.text

    def build_chat_prompt(
        self,
        history,
        user_message
    ):

        prompt = ""

        for message in history:

            prompt += (
                f"{message.role}: "
                f"{message.content}\n"
            )

        prompt += f"user: {user_message}\n"
        prompt += "assistant:"

        return prompt

    def chat(
        self,
        history,
        user_message
    ):

        prompt = self.build_chat_prompt(
            history,
            user_message
        )

        return self.generate(prompt)