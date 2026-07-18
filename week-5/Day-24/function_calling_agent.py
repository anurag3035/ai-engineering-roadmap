import json

from google.genai import types

from gemini_client import GeminiClient
from tools import (
    get_current_date,
    calculator,
    search_knowledge_base,
)


client = GeminiClient()


def execute_tool(function_call):

    tool_name = function_call.name
    arguments = dict(function_call.args)

    print("\n" + "=" * 50)
    print("Tool Called :", tool_name)
    print("Arguments   :", arguments)

    if tool_name == "get_current_date":
        result = get_current_date()

    elif tool_name == "calculator":
        result = calculator(arguments["expression"])

    elif tool_name == "search_knowledge_base":
        result = search_knowledge_base(arguments["query"])

    else:
        result = "Unknown tool."

    print("Tool Result :", result)

    return types.Part.from_function_response(
        name=tool_name,
        response={
            "result": result
        }
    )
def run_agent():

    print("=" * 60)
    print("Gemini Function Calling Agent")
    print("=" * 60)

    while True:

        user_input = input("\nYou : ")

        if user_input.lower() in ["exit", "quit"]:
            print("\nGoodbye!")
            break

        response = client.generate(user_input)

        if not response.function_calls:

            print("\nAssistant :")
            print(response.text)
            continue

        function_responses = []

        for function_call in response.function_calls:

            function_response = execute_tool(function_call)

            function_responses.append(function_response)

        response = client.client.models.generate_content(
            model=client.model,
            contents=[
                user_input,
                response.candidates[0].content,
                types.Content(
                    role="tool",
                    parts=function_responses
                ),
            ],
        )

        print("\nAssistant :")
        print(response.text)
if __name__ == "__main__":
    run_agent()
