from gemini_client import GeminiClient


def text_generation_demo(client):
    print("\n" + "=" * 60)
    print("TEXT GENERATION")
    print("=" * 60)

    prompt = "Explain Artificial Intelligence in simple words."

    response = client.generate_text(prompt)

    print("\nQuestion:")
    print(prompt)

    print("\nAnswer:")
    print(response)


def chat_demo(client):
    print("\n" + "=" * 60)
    print("CHAT SESSION")
    print("=" * 60)

    chat = client.start_chat()

    question1 = "Hi! My name is Anurag."

    answer1 = client.chat(chat, question1)

    print("\nYou:", question1)
    print("Gemini:", answer1)

    question2 = "Do you remember my name?"

    answer2 = client.chat(chat, question2)

    print("\nYou:", question2)
    print("Gemini:", answer2)


def token_demo(client):
    print("\n" + "=" * 60)
    print("TOKEN COUNT")
    print("=" * 60)

    text = "Artificial Intelligence is changing the world."

    total_tokens = client.count_tokens(text)

    print(f"\nPrompt: {text}")
    print(f"Tokens Used: {total_tokens}")


def image_demo(client):
    print("\n" + "=" * 60)
    print("IMAGE ANALYSIS")
    print("=" * 60)

    try:
        response = client.analyze_image(
            "sample.jpg",
            "Describe this image in detail."
        )

        print("\nGemini:")
        print(response)

    except FileNotFoundError:
        print("sample.jpg not found.")
        print("Place any image named 'sample.jpg' in this folder.")


def main():

    client = GeminiClient()

    text_generation_demo(client)

    chat_demo(client)

    token_demo(client)

    image_demo(client)


if __name__ == "__main__":
    main()