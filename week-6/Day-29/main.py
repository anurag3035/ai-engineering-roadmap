from gemini_client_v3 import GeminiClientV3


def main():

    client = GeminiClientV3()

    print("=" * 50)
    print("Gemini Safety & Cost Control")
    print("=" * 50)

    while True:

        prompt = input("\nYou : ")

        if prompt.lower() == "exit":
            break

        response = client.generate(prompt)

        print("\nGemini :", response)

    client.usage_report()


if __name__ == "__main__":
    main()