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

**Location:**
- Gemini CLI: `.gemini/skills/video-to-minutes/`
- Codex: `.codex/skills/video-to-minutes/`

**Usage (Codex):**
```text
Use $video-to-minutes to convert this meeting video into concise minutes.
```

**Dependencies:** `ffmpeg`, `faster-whisper`

### gh-security-scan

Investigates security incidents across GitHub enterprise, organization, or repository scope and documents findings in tracking issues.

**Location:**
- Claude Code: `.claude/skills/gh-security-scan/`
- Codex: `.codex/skills/gh-security-scan/`
- Gemini CLI: `.gemini/skills/gh-security-scan/`

**Usage (Claude Code):**
```text
/gh-security-scan --org my-org "CVE-2025-12345: check for vulnerable versions"
```

**Usage (Codex):**
```text
Use $gh-security-scan with --org my-org "CVE-2025-12345: check for vulnerable versions".
```

**Usage (Gemini CLI):**
```text
Check for vulnerable library versions related to CVE-2025-12345 in the --org my-org
```

**Dependencies:** GitHub access via Codex GitHub app or `gh`

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
├── .claude/
│   ├── settings.local.json
│   └── skills/
│       ├── gh-security-scan/
│       │   ├── SKILL.md
│       │   └── references/
│       │       └── investigation_patterns.md
│       └── security-scan/
├── .codex/
│   └── skills/
│       ├── gh-security-scan/
│       │   ├── SKILL.md
│       │   └── references/
│       │       └── investigation-patterns-guide.md
│       └── video-to-minutes/
│           ├── SKILL.md
│           ├── agents/
│           │   └── openai.yaml
│           └── scripts/
│               └── transcribe.py
├── .gemini/
│   └── skills/
│       ├── gh-security-scan/
│       │   ├── SKILL.md
│       │   └── references/
│       │       └── investigation_patterns.md
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
├── .qodo/
│   ├── agents/
│   └── workflows/
├── LICENSE
└── README.md
```

## Contributing

Contributions are welcome! Feel free to submit pull requests with new skills or improvements to existing ones.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
