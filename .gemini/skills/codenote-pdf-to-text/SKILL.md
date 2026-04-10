---
name: codenote-pdf-to-text
description: Extracts text content from PDF files. Use this skill when you need to convert a PDF document into plain text for further processing or analysis.
---

# PDF to Text Converter

## Overview

This skill provides the capability to extract all textual content from a given PDF file and present it as plain text.

## Workflow

To extract text from a PDF, follow these steps:

1.  **Provide the PDF file path**: Specify the absolute path to the PDF document you wish to process.
2.  **Execute the script**: The `scripts/extract_text.py` script will be used to perform the extraction.

## Usage Example

To extract text from a PDF file named `document.pdf` located at `/path/to/document.pdf`, you would instruct the agent to "Extract text from the PDF file at `/path/to/document.pdf`".

## Resources

### scripts/
- `extract_text.py`: A Python script that takes a PDF file path as input and outputs its textual content to standard output.
