# Day-32: Chunking Strategies Comparison

## Overview

This project compares four popular chunking strategies used in Retrieval-Augmented Generation (RAG) systems.

## Chunking Strategies

- Fixed-size Chunking
- Recursive Character Chunking
- Sentence-aware Chunking
- Semantic Chunking

## Features

- Compare multiple chunking techniques
- Display chunk statistics
- Generate a comparison report
- Demonstrate the impact of chunking on document preparation for RAG

## Requirements

```bash
pip install -r requirements.txt
```

## Run

```bash
python chunking_comparison.py
```

## Output

The program:

- Reads `sample.txt`
- Applies four chunking strategies
- Displays statistics
- Generates `chunking_report.md`

## Project Structure

```
Day-32/
│
├── chunking_comparison.py
├── chunking_report.md
├── sample.txt
├── requirements.txt
└── README.md
```