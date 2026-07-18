from google import genai
from google.genai import types

from config import GEMINI_API_KEY, MODEL_NAME


class GeminiClient:

    def __init__(self):

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        self.model = MODEL_NAME

        self.tools = [
            types.Tool(
                function_declarations=[
                    types.FunctionDeclaration(
                        name="get_current_date",
                        description="Returns today's current date.",
                        parameters_json_schema={
                            "type": "object",
                            "properties": {}
                        }
                    ),
                    types.FunctionDeclaration(
                        name="calculator",
                        description="Evaluate a mathematical expression.",
                        parameters_json_schema={
                            "type": "object",
                            "properties": {
                                "expression": {
                                    "type": "string",
                                    "description": "Mathematical expression."
                                }
                            },
                            "required": [
                                "expression"
                            ]
                        }
                    ),
                    types.FunctionDeclaration(
                        name="search_knowledge_base",
                        description="Search the local knowledge base.",
                        parameters_json_schema={
                            "type": "object",
                            "properties": {
                                "query": {
                                    "type": "string",
                                    "description": "Search query."
                                }
                            },
                            "required": [
                                "query"
                            ]
                        }
                    )
                ]
            )
        ]

    def generate(self, prompt):

        print("MODEL =", self.model)
        print("API KEY FOUND =", GEMINI_API_KEY is not None)

        return 
        self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=self.tools
            )
        )