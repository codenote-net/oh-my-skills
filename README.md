# Oh My Skills

A curated collection of skills and plugins for AI coding assistants.

## Overview

Oh My Skills provides reusable skills for AI-powered development tools. These skills extend the capabilities of your AI coding assistant, enabling automated workflows for common tasks like document processing and data transformation.

## Supported AI Tools

| Tool | Namespace | Config Directory | Status |
|------|-----------|------------------|--------|
| [Claude Code](https://github.com/anthropics/claude-code) | `codenote:` (plugin) | `plugins/codenote/` | Active |
| [Codex](https://github.com/openai/codex) | `codenote:` (plugin) | `.codex/` | Active |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | `codenote-` (prefix) | `.gemini/` | Active |

## Available Skills

### codenote-pdf-to-text

Extracts text content from PDF files using PyPDF2.

**Location:** `.gemini/skills/codenote-pdf-to-text/`

**Usage:**
```bash
python scripts/extract_text.py <pdf_file_path>
```

**Dependencies:** `PyPDF2`

### codenote-text-to-excel

Converts text data (especially Markdown tables) into Excel spreadsheets using openpyxl.

**Location:** `.gemini/skills/codenote-text-to-excel/`

**Usage:**
```bash
# Basic usage
python scripts/text_to_excel.py <input.txt> <output.xlsx>

# With template
python scripts/text_to_excel.py <input.txt> <output.xlsx> --template <template.xlsx>
```

**Dependencies:** `openpyxl`

### codenote:video-to-minutes

Extracts audio and images from a video file, transcribes the audio using Whisper, and generates structured meeting minutes.

**Location:**
- Gemini CLI: `.gemini/skills/codenote-video-to-minutes/`
- Codex: `.codex/skills/video-to-minutes/`

**Usage (Codex):**
```text
Use $codenote:video-to-minutes to convert this meeting video into concise minutes.
```

**Dependencies:** `ffmpeg`, `faster-whisper`

### codenote:gh-security-scan

Investigates security incidents across GitHub enterprise, organization, or repository scope and documents findings in tracking issues.

**Location:**
- Claude Code: `plugins/codenote/skills/gh-security-scan/`
- Codex: `.codex/skills/gh-security-scan/`
- Gemini CLI: `.gemini/skills/codenote-gh-security-scan/`

**Usage (Claude Code):**
```text
/codenote:gh-security-scan --org my-org "CVE-2025-12345: check for vulnerable versions"
```

**Usage (Codex):**
```text
Use $codenote:gh-security-scan with --org my-org "CVE-2025-12345: check for vulnerable versions".
```

**Usage (Gemini CLI):**
```text
Check for vulnerable library versions related to CVE-2025-12345 in the --org my-org
```

**Dependencies:** GitHub access via Codex GitHub app or `gh`

## Installation

### Claude Code (plugin)

```bash
# Load as a plugin (skills appear as codenote:skill-name)
claude --plugin-dir ./plugins/codenote
```

### Codex

Copy `.codex/` to your project root. The `.codex-plugin/plugin.json` provides the `codenote:` namespace automatically.

### Gemini CLI

Copy `.gemini/skills/codenote-*/` to your project's `.gemini/skills/` directory.

### Python dependencies

```bash
pip install PyPDF2 openpyxl faster-whisper
```

## Project Structure

```
oh-my-skills/
├── .claude-plugin/
│   └── marketplace.json              # Claude Code marketplace manifest
├── plugins/
│   └── codenote/                     # Claude Code plugin (namespace: codenote:)
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── skills/
│       │   └── gh-security-scan/
│       │       ├── SKILL.md
│       │       └── references/
│       │           └── investigation_patterns.md
│       └── commands/
│           └── gh-security-scan.md
├── .codex/
│   ├── .codex-plugin/
│   │   └── plugin.json               # Codex plugin (namespace: codenote:)
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
│   └── skills/                        # Gemini CLI (prefix: codenote-)
│       ├── codenote-gh-security-scan/
│       │   ├── SKILL.md
│       │   └── references/
│       │       └── investigation_patterns.md
│       ├── codenote-pdf-to-text/
│       │   ├── SKILL.md
│       │   └── scripts/
│       │       └── extract_text.py
│       ├── codenote-text-to-excel/
│       │   ├── SKILL.md
│       │   ├── scripts/
│       │   │   └── text_to_excel.py
│       │   └── references/
│       │       ├── excel_template_guide.md
│       │       └── parsing_rules_guide.md
│       └── codenote-video-to-minutes/
│           ├── SKILL.md
│           └── scripts/
│               └── transcribe.py
├── LICENSE
└── README.md
```

## Contributing

Contributions are welcome! Feel free to submit pull requests with new skills or improvements to existing ones.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
