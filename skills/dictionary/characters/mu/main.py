#!/usr/bin/env python3
"""
幕 (mu) - 生成字幕
"""

import sys
import json


def execute(params):
    text = params.get("text", "").strip()
    if not text:
        return {"status": "error", "message": "Text cannot be empty"}

    format_type = params.get("format", "srt")
    duration = params.get("duration", 3)

    sentences = [s.strip() for s in text.split("\n") if s.strip()]

    subtitle = ""
    for i, sentence in enumerate(sentences, 1):
        start = (i - 1) * duration
        end = i * duration

        if format_type == "srt":
            subtitle += f"{i}\n"
            subtitle += f"{format_time(start)} --> {format_time(end)}\n"
            subtitle += f"{sentence}\n\n"
        elif format_type == "vtt":
            subtitle += f"{format_time(start)} --> {format_time(end)}\n"
            subtitle += f"{sentence}\n\n"

    return {"status": "success", "data": {"subtitle": subtitle, "format": format_type}}


def format_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


if __name__ == "__main__":
    try:
        params = json.loads(sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read())
        print(json.dumps(execute(params), ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)
