import re


class TextCleaner:

    @staticmethod
    def clean(text: str) -> str:

        text = text.replace("\r", "")

        text = re.sub(r"-\n", "", text)

        text = re.sub(r"\n+", "\n", text)

        text = re.sub(r"[ \t]+", " ", text)

        text = re.sub(r"\n\s+", "\n", text)

        text = re.sub(r"[^\x20-\x7E\n]", "", text)

        return text.strip()