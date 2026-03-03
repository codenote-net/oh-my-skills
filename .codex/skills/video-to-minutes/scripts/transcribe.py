import argparse
import sys


def format_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:05.2f}"


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe audio using faster-whisper."
    )
    parser.add_argument("audio_path", help="Path to the audio file to transcribe.")
    parser.add_argument(
        "--language", default="ja", help="Language code (default: ja)"
    )
    parser.add_argument(
        "--model", default="large-v3", help="Whisper model name (default: large-v3)"
    )
    parser.add_argument(
        "--output",
        default="meeting_audio.txt",
        help="Output text file path (default: meeting_audio.txt)",
    )
    parser.add_argument(
        "--device", default="cpu", help="Device to use (default: cpu)"
    )
    parser.add_argument(
        "--compute-type",
        default="int8",
        help="Compute type for quantization (default: int8)",
    )
    parser.add_argument(
        "--beam-size", type=int, default=5, help="Beam size (default: 5)"
    )
    parser.add_argument(
        "--cpu-threads",
        type=int,
        default=0,
        help="Number of CPU threads for CTranslate2 (default: auto)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=0,
        help="Enable batched inference when > 0 (default: disabled)",
    )
    args = parser.parse_args()

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print(
            "Error: faster-whisper is not installed.\n"
            "Install it with: pip install faster-whisper",
            file=sys.stderr,
        )
        sys.exit(1)

    print(
        f"Loading model '{args.model}' on {args.device} ({args.compute_type})...",
        flush=True,
    )
    model_kwargs = {"device": args.device, "compute_type": args.compute_type}
    if args.cpu_threads > 0:
        model_kwargs["cpu_threads"] = args.cpu_threads
    model = WhisperModel(args.model, **model_kwargs)

    print(
        f"Transcribing '{args.audio_path}' (language={args.language}, beam_size={args.beam_size})...",
        flush=True,
    )
    transcribe_kwargs = {"language": args.language, "beam_size": args.beam_size}
    if args.batch_size > 0:
        try:
            from faster_whisper import BatchedInferencePipeline
        except ImportError:
            print(
                "Warning: BatchedInferencePipeline is unavailable, falling back to non-batched mode.",
                flush=True,
            )
            segments, info = model.transcribe(args.audio_path, **transcribe_kwargs)
        else:
            print(
                f"Using batched inference (batch_size={args.batch_size})...",
                flush=True,
            )
            batched_model = BatchedInferencePipeline(model=model)
            segments, info = batched_model.transcribe(
                args.audio_path, batch_size=args.batch_size, **transcribe_kwargs
            )
    else:
        segments, info = model.transcribe(args.audio_path, **transcribe_kwargs)

    print(
        f"Detected language: {info.language} (probability {info.language_probability:.2f})",
        flush=True,
    )

    lines = []
    for segment in segments:
        line = segment.text.strip()
        print(
            f"[{format_time(segment.start)} -> {format_time(segment.end)}] {line}",
            flush=True,
        )
        lines.append(line)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"\nTranscription saved to '{args.output}'", flush=True)


if __name__ == "__main__":
    main()
