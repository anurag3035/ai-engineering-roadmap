import pytest
import asyncio

from chunker_strategy import (
    FixedSizeChunker,
    SentenceChunker,
    RecursiveChunker
)


@pytest.mark.parametrize(
    "text,size,expected",
    [
        ("abcdefghij", 5, ["abcde", "fghij"]),
        ("hello", 2, ["he", "ll", "o"]),
        ("python", 10, ["python"])
    ]
)
def test_fixed_size_chunker(text, size, expected):
    chunker = FixedSizeChunker(size)
    assert chunker.chunk(text) == expected


@pytest.mark.parametrize(
    "text,expected_count",
    [
        ("A. B. C.", 3),
        ("Hello world.", 1),
        ("One. Two.", 2)
    ]
)
def test_sentence_chunk_count(text, expected_count):
    chunker = SentenceChunker()
    result = chunker.chunk(text)

    assert len(result) == expected_count


def test_sentence_chunk_content():
    chunker = SentenceChunker()

    result = chunker.chunk("Python is great. AI is growing.")

    assert result == [
        "Python is great",
        "AI is growing"
    ]


def test_recursive_chunker_returns_list():
    chunker = RecursiveChunker(20)

    result = chunker.chunk(
        "Python is used for artificial intelligence"
    )

    assert isinstance(result, list)


def test_recursive_chunker_not_empty():
    chunker = RecursiveChunker(20)

    result = chunker.chunk(
        "Python is used for artificial intelligence"
    )

    assert len(result) > 0


@pytest.mark.parametrize(
    "text,max_length",
    [
        ("hello world python", 10),
        ("one two three four", 15),
        ("artificial intelligence", 12)
    ]
)
def test_recursive_chunk_size(text, max_length):
    chunker = RecursiveChunker(max_length)

    result = chunker.chunk(text)

    for chunk in result:
        assert len(chunk) <= max_length


def test_fixed_size_empty_string():
    chunker = FixedSizeChunker(5)

    assert chunker.chunk("") == []


def test_sentence_empty_string():
    chunker = SentenceChunker()

    assert chunker.chunk("") == []


def test_recursive_empty_string():
    chunker = RecursiveChunker(10)

    assert chunker.chunk("") == []


def test_fixed_size_single_chunk():
    chunker = FixedSizeChunker(20)

    result = chunker.chunk("hello")

    assert result == ["hello"]


def test_sentence_no_period():
    chunker = SentenceChunker()

    result = chunker.chunk("Hello World")

    assert result == ["Hello World"]


def test_recursive_single_word():
    chunker = RecursiveChunker(20)

    result = chunker.chunk("Python")

    assert result == ["Python"]


async def async_chunk():
    await asyncio.sleep(0.1)

    chunker = FixedSizeChunker(3)

    return chunker.chunk("abcdef")


@pytest.mark.asyncio
async def test_async_chunking():
    result = await async_chunk()

    assert result == ["abc", "def"]