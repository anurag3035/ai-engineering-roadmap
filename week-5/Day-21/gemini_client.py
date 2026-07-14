import logging
import google.generativeai as genai

from config import GEMINI_API_KEY


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)


class GeminiClient:

    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)

    def generate_response(
        self,
        prompt: str,
        system_prompt: str,
        temperature: float = 0.7
    ):

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=system_prompt,
            generation_config={
                "temperature": temperature
            }
        )

        logging.info(f"Temperature : {temperature}")

        response = model.generate_content(prompt)

        return response.text