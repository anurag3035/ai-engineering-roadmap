# Day-31: Multi-Format Document Loader

## Overview

This project implements a reusable `DocumentLoader` class that loads documents from multiple file formats and converts them into a common `Document(content, metadata)` representation.

## Supported Formats

- PDF (.pdf)
- Microsoft Word (.docx)
- Text (.txt)

## Features

- Extract text from PDF, DOCX, and TXT files
- Clean extracted text
- Generate metadata
- Return reusable Document objects
- Modular code structure

## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
python test_loader.py
```

## Example Output

```
Loading: sample.pdf

Metadata:
source: sample.pdf
page: 1
doc_type: pdf
word_count: 120
char_count: 840

Content Preview:
Artificial Intelligence is transforming industries...
```

## Project Structure

```
Day-31/
│
├── cleaner.py
├── document_loader.py
├── models.py
├── test_loader.py
├── sample.pdf
├── sample.docx
├── sample.txt
├── requirements.txt
└── README.md
```