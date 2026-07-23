from chat_session import ChatSession


def main():

    print("=" * 50)
    print("Conversation Memory Demo")
    print("=" * 50)

    session_id = input("Session ID: ")

    chat = ChatSession(session_id)

    print("\nType 'exit' to quit.\n")

    while True:

        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        response = chat.chat(user_input)

        print("\nAssistant:")
        print(response)
        print()


if __name__ == "__main__":
    main()