---
name: video-to-minutes
description: Extracts audio and images from a video file, transcribes the audio, and generates meeting minutes and a summary.
---

# Video to Minutes Skill

This skill guides the process of converting a video recording of a meeting into a structured Markdown file containing meeting minutes, a summary, and references to captured images.

## Workflow

The process is sequential. Follow these steps in order.

### 1. Prerequisite Check

This workflow depends on `ffmpeg` (command-line tool) and `faster-whisper` (Python package).

First, check if these are installed:

```bash
which ffmpeg
python -c "from faster_whisper import WhisperModel; print('faster-whisper is installed')"
```

- If both commands succeed, the tools are installed. Proceed to the next step.
- If either fails, the tool is missing. Ask the user for permission to install them.

```bash
# Install ffmpeg (macOS with Homebrew)
brew install ffmpeg
# Install faster-whisper
pip install faster-whisper
```
Confirm successful installation before proceeding.

### 2. Get User Input

- **Video File Path:** Ask the user for the full path to the video file they want to process.
- **Capture Interval:** Ask the user for the desired interval in seconds for capturing images (e.g., 60 for every minute, 300 for every 5 minutes). Suggest a default of `60` seconds. If the user does not specify an interval, ask for confirmation to use `60` seconds.

### 3. Audio Extraction

Use `ffmpeg` to extract the audio from the video file into a `wav` file format, which is ideal for transcription. Save it in the current working directory.

**Command Template:**
```bash
ffmpeg -i "<VIDEO_FILE_PATH>" -vn -acodec pcm_s16le -ar 16000 -ac 1 meeting_audio.wav
```
- Replace `<VIDEO_FILE_PATH>` with the path provided by the user.
- The output file will be `meeting_audio.wav`.

### 4. Audio Transcription (Automated)

The skill uses `faster-whisper` via a Python script to transcribe the extracted audio. Since transcription is time-intensive, this step uses background execution to prevent tool timeouts.

**Important:** For videos longer than 5 minutes or audio files exceeding 20MB, you **must** run the transcription in the background. Running it in the foreground risks process cancellation due to tool timeouts.

**Step 4a: Start transcription in the background**

Redirect output to a log file and run in the background using `is_background: true`:

```bash
python scripts/transcribe.py meeting_audio.wav --language ja --model large-v3 > meeting_audio.log 2>&1
```
(Execute with `is_background: true`. The language and model can be adjusted if required, but the default will be Japanese and 'large-v3' model.)

**Step 4b: Monitor progress and wait for completion**

Monitor the log file to track progress and detect completion. The script outputs `[start -> end] text` for each segment in real-time:

```bash
tail -f meeting_audio.log
```

The transcription is complete when you see `Transcription saved to` in the log. You can also check if the process is still running:

```bash
ps aux | grep transcribe.py
```

The script will generate `meeting_audio.txt` in the current working directory. The skill will automatically detect this file upon completion.

### 4.5. Detect Transcription File

1.  The skill will first attempt to find `meeting_audio.txt` in the current working directory.
2.  If found, its path will be automatically used.
3.  If not found, the user will be prompted to provide the full path to the `meeting_audio.txt` file.

### 5. Image Extraction

While the user is running the transcription (or after), you can extract the images.

1.  Create a directory to store the images.
    ```bash
    mkdir captures
    ```
2.  Use `ffmpeg` to extract frames from the video at the interval specified by the user.

**Command Template:**
```bash
ffmpeg -i "<VIDEO_FILE_PATH>" -vf fps=1/<INTERVAL_IN_SECONDS> captures/capture_%03d.png
```
- Replace `<VIDEO_FILE_PATH>` with the user's video path.
- Replace `<INTERVAL_IN_SECONDS>` with the interval provided by the user.

### 5.5. Collect Proper Nouns

Before generating the meeting minutes, the skill will ask the user to provide a list of key proper nouns (e.g., names of people, companies, products like "重岡", "株式会社ROUTE06", "ProjectX") that are likely to appear in the meeting. This information will be incorporated into the prompt for generating the minutes to improve accuracy and reduce errors in transcription and summarization.

### 6. Generate Meeting Minutes

1.  The content of the `meeting_audio.txt` will be used for transcription.
2.  List the newly created image files in the `captures` directory.
3.  Analyze the transcript to identify participants, key topics, decisions, and action items.
4.  Synthesize this information into a clear and structured Markdown format, including:
    - A high-level summary.
    - A detailed "Meeting Minutes" section with participants, purpose, key decisions, and next actions.
    - A "Reference: List of Capture Images" section listing all the files in the `captures` directory.

### 7. Save the Output

Save the final generated Markdown content to a file named `meeting_minutes.md`.

```bash
write_file(file_path="meeting_minutes.md", content="<MARKDOWN_CONTENT>")
```
Inform the user that the process is complete and the file has been saved.
