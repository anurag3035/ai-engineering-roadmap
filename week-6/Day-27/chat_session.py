from gemini_client import GeminiClient
from storage import SessionStorage
from summarizer import Summarizer
from config import MAX_MESSAGES, SUMMARY_TRIGGER


class ChatSession:

    def __init__(self, session_id):

        self.client = GeminiClient()
        self.storage = SessionStorage()
        self.summarizer = Summarizer()

        self.session_id = session_id

        self.messages = self.storage.load(session_id)

    def add_message(self, role, content):

        self.messages.append(
            {
                "role": role,
                "content": content
            }
        )

    def build_prompt(self):

        prompt = ""

        for message in self.messages:

            prompt += (
                f"{message['role']}: "
                f"{message['content']}\n"
            )

        prompt += "assistant:"

        return prompt

    def summarize_history(self):

        if len(self.messages) < SUMMARY_TRIGGER:
            return

        old_messages = self.messages[:-4]

        summary = self.summarizer.summarize(old_messages)

        self.messages = [
            {
                "role": "system",
                "content": f"Conversation Summary:\n{summary}"
            }
        ] + self.messages[-4:]

    def trim_history(self):

        if len(self.messages) > MAX_MESSAGES:

            self.messages = self.messages[-MAX_MESSAGES:]

    def chat(self, user_input):

        self.add_message(
            "user",
            user_input
        )

        self.summarize_history()

        self.trim_history()

        prompt = self.build_prompt()

        response = self.client.generate(prompt)

        self.add_message(
            "assistant",
            response
        )

        self.storage.save(
            self.session_id,
            self.messages
        )

        return response