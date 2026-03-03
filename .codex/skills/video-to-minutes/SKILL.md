---
name: video-to-minutes
description: Convert meeting recordings into structured Markdown minutes by extracting audio and screenshots, transcribing speech with faster-whisper, and drafting summary/decisions/action items. Use when Codex is asked to turn a video file (mp4/mov/mkv/webm) into meeting notes, summaries, or minutes.
---

# Video to Minutes

## Overview

Convert a meeting video into `meeting_minutes.md` with a reliable, repeatable workflow.
Use `ffmpeg` for audio/frame extraction and `scripts/transcribe.py` for transcription.

## Workflow

Execute the steps in order.

### 1. Validate Prerequisites

Run:

```bash
which ffmpeg
python3 -c "from faster_whisper import WhisperModel; print('faster-whisper: ok')"
```

If either check fails, ask for permission before installing missing dependencies.

### 2. Collect Inputs

Ask for:
- Absolute path to the video file.
- Screenshot interval in seconds (default `60`).
- Transcription language code (default `ja`).
- Optional CPU thread count for transcription (`cpu_threads`, default auto).
- Optional batch size for batched inference (`batch_size`, default disabled).
- Important proper nouns (people, company names, product names).
- Output Markdown path (default `meeting_minutes.md`).

### 3. Prepare Working Files

Run in the current working directory:

```bash
ffmpeg -i "<VIDEO_FILE_PATH>" -vn -acodec pcm_s16le -ar 16000 -ac 1 meeting_audio.wav
mkdir -p captures
ffmpeg -i "<VIDEO_FILE_PATH>" -vf fps=1/<INTERVAL_SECONDS> captures/capture_%03d.png
```

### 4. Transcribe Audio

Use:

```bash
python3 scripts/transcribe.py meeting_audio.wav \
  --language "<LANGUAGE_CODE>" \
  --model large-v3 \
  --cpu-threads <CPU_THREADS_OR_0> \
  --batch-size <BATCH_SIZE_OR_0> \
  --output meeting_audio.txt \
  > meeting_audio.log 2>&1
```

For long videos, run in background and monitor progress:

```bash
python3 scripts/transcribe.py meeting_audio.wav --language "<LANGUAGE_CODE>" --model large-v3 --cpu-threads <CPU_THREADS_OR_0> --batch-size <BATCH_SIZE_OR_0> --output meeting_audio.txt > meeting_audio.log 2>&1 &
tail -f meeting_audio.log
```

Wait until the log includes `Transcription saved to` and confirm `meeting_audio.txt` exists.

### 5. Draft Minutes

Read `meeting_audio.txt` and list files in `captures/`.
Generate concise minutes grounded in transcript content. Do not invent facts.
Use provided proper nouns to correct likely transcription mistakes.

Use this output structure:

```markdown
# Meeting Summary

## Highlights
- ...

## Decisions
- ...

## Action Items
| Assignee | Task | Due |
| --- | --- | --- |
| TBD | ... | TBD |

## Detailed Minutes
- ...

## Reference: Capture Images
- captures/capture_001.png
- ...
```

### 6. Save Deliverable

Write the final Markdown to the requested output path (default `meeting_minutes.md`).
Report completion with:
- Output file path
- Transcript file path
- Number of capture images found

## Resources

### scripts/
- `transcribe.py`: faster-whisper based transcription utility that prints progress and saves plain-text transcript.
