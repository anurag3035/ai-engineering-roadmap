import json
import os

from config import SESSION_FOLDER


class SessionStorage:

    def __init__(self):

        os.makedirs(
            SESSION_FOLDER,
            exist_ok=True
        )

    def save(self, session_id, messages):

        filename = os.path.join(
            SESSION_FOLDER,
            f"{session_id}.json"
        )

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                messages,
                file,
                indent=4,
                ensure_ascii=False
            )

    def load(self, session_id):

        filename = os.path.join(
            SESSION_FOLDER,
            f"{session_id}.json"
        )

        if not os.path.exists(filename):
            return []

        with open(
            filename,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)