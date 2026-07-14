from gemini_client import GeminiClient

client = GeminiClient()

question = "Explain Artificial Intelligence in simple words."

system_prompts = [
    "You are a school teacher.",
    "You are a software engineer.",
    "You are a funny comedian."
]

temperatures = [0.0, 0.3, 0.7, 1.0]

for prompt in system_prompts:

    print("=" * 70)
    print(prompt)
    print("=" * 70)

    for temp in temperatures:

        print(f"\nTemperature : {temp}")

        answer = client.generate_response(
            question,
            prompt,
            temp
        )

        print(answer)
        print("-" * 70)