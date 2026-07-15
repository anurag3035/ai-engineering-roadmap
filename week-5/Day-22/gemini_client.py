import logging
from pathlib import Path

import google.generativeai as genai
from PIL import Image
from tenacity import retry, stop_after_attempt, wait_exponential

from config import (
    GEMINI_API_KEY,
    MODEL_NAME,
    TEMPERATURE,
    TOP_P,
    TOP_K,
    MAX_OUTPUT_TOKENS,
    MAX_INPUT_TOKENS
)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
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
                "max_output_tokens": MAX_OUTPUT_TOKENS
            },
            system_instruction=(
                "You are a helpful AI assistant. "
                "Answer clearly and accurately."
            )
        )

        logging.info("Gemini Client Initialized")


    def count_tokens(self, text: str):

        """
        Counts tokens in the prompt.
        """

        result = self.model.count_tokens(text)

        logging.info(f"Prompt Tokens : {result.total_tokens}")

        return result.total_tokens


    def check_budget(self, text: str):

        """
        Prevent very large prompts.
        """

        total_tokens = self.count_tokens(text)

        if total_tokens > MAX_INPUT_TOKENS:
            raise ValueError(
                f"Prompt too large ({total_tokens} tokens). "
                f"Limit is {MAX_INPUT_TOKENS}."
            )


    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=2)
    )
    def generate_text(self, prompt: str):

        """
        Generate a text response.
        """

        self.check_budget(prompt)

        logging.info("Generating response...")

        response = self.model.generate_content(prompt)

        logging.info("Response generated successfully.")

        return response.text


    def start_chat(self):

        """
        Create a chat session.
        """

        logging.info("Starting chat session...")

        return self.model.start_chat(history=[])


    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=2)
    )
    def chat(self, chat_session, message: str):

        """
        Continue a conversation.
        """

        self.check_budget(message)

        response = chat_session.send_message(message)

        return response.text


    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=2)
    )
    def analyze_image(self, image_path: str, prompt: str):

        """
        Image + Text (Multimodal)
        """

        image = Image.open(Path(image_path))

        response = self.model.generate_content(
            [
                prompt,
                image
            ]
        )

        return response.text