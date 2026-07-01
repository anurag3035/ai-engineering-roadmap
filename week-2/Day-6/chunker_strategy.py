from abc import ABC, abstractmethod


class Chunker(ABC):
    @abstractmethod
    def chunk(self, text):
        pass


class FixedSizeChunker(Chunker):
    def __init__(self, size):
        self.size = size

    def chunk(self, text):
        chunks = []

        for i in range(0, len(text), self.size):
            chunks.append(text[i:i + self.size])

        return chunks


class SentenceChunker(Chunker):
    def chunk(self, text):
        sentences = text.split(".")

        chunks = []

        for sentence in sentences:
            sentence = sentence.strip()

            if sentence:
                chunks.append(sentence)

        return chunks


class RecursiveChunker(Chunker):
    def __init__(self, max_length):
        self.max_length = max_length

    def chunk(self, text):
        words = text.split()
        chunks = []
        current_chunk = ""

        for word in words:
            if len(current_chunk + " " + word) <= self.max_length:
                current_chunk += " " + word
            else:
                chunks.append(current_chunk.strip())
                current_chunk = word

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks


def process_text(chunker, text):
    return chunker.chunk(text)


sample_text = """
Python is a popular programming language. It is widely used in AI and machine learning.
Design patterns help make code flexible and maintainable.
"""


strategies = [
    FixedSizeChunker(30),
    SentenceChunker(),
    RecursiveChunker(40)
]


for strategy in strategies:
    print(f"\nUsing {strategy.__class__.__name__}")

    result = process_text(strategy, sample_text)

    for index, chunk in enumerate(result, start=1):
        print(f"Chunk {index}: {chunk}")