# Oh My Skills

A curated collection of skills and plugins for AI coding assistants.

## Overview

Oh My Skills provides reusable skills for AI-powered development tools. These skills extend the capabilities of your AI coding assistant, enabling automated workflows for common tasks like document processing and data transformation.

## Supported AI Tools

| Tool | Config Directory | Status |
|------|------------------|--------|
| [Claude Code](https://github.com/anthropics/claude-code) | `.claude/` | Active |
| [Codex](https://github.com/openai/codex) | `.codex/` | Active |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | `.gemini/` | Active |

## Available Skills

### pdf-to-text

Extracts text content from PDF files using PyPDF2.

**Location:** `.gemini/skills/pdf-to-text/`

**Usage:**
```bash
python scripts/extract_text.py <pdf_file_path>
```

**Dependencies:** `PyPDF2`

### text-to-excel

Converts text data (especially Markdown tables) into Excel spreadsheets using openpyxl.

**Location:** `.gemini/skills/text-to-excel/`

**Usage:**
```bash
# Basic usage
python scripts/text_to_excel.py <input.txt> <output.xlsx>

# With template
python scripts/text_to_excel.py <input.txt> <output.xlsx> --template <template.xlsx>
```

**Dependencies:** `openpyxl`

### video-to-minutes

Extracts audio and images from a video file, transcribes the audio using Whisper, and generates structured meeting minutes.

**Location:** `.gemini/skills/video-to-minutes/`

**Dependencies:** `ffmpeg`, `faster-whisper`

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/codenote-net/oh-my-skills.git
   ```

2. Copy the desired skill directories to your project's AI tool configuration folder.

3. Install Python dependencies as needed:
   ```bash
   pip install PyPDF2 openpyxl faster-whisper
   ```

## Project Structure

```
oh-my-skills/
├── .gemini/
│   └── skills/
│       ├── pdf-to-text/
│       │   ├── SKILL.md
│       │   └── scripts/
│       │       └── extract_text.py
│       ├── text-to-excel/
│       │   ├── SKILL.md
│       │   ├── scripts/
│       │   │   └── text_to_excel.py
│       │   └── references/
│       │       ├── excel_template_guide.md
│       │       └── parsing_rules_guide.md
│       └── video-to-minutes/
│           ├── SKILL.md
│           └── scripts/
│               └── transcribe.py
├── .claude/
│   └── settings.local.json
├── .qodo/
│   ├── agents/
│   └── workflows/
└── LICENSE
```

## Contributing

Contributions are welcome! Feel free to submit pull requests with new skills or improvements to existing ones.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
