#!/usr/bin/env python3
"""
听 (ting) - 语音识别
"""

import sys
import json

try:
    import speech_recognition as sr
except ImportError:
    print(
        json.dumps(
            {"status": "error", "message": "Missing: pip install SpeechRecognition"}
        )
    )
    sys.exit(1)


def execute(params):
    audio_path = params.get("audio", "").strip()
    if not audio_path:
        return {"status": "error", "message": "Audio path required"}

    language = params.get("language", "zh-CN")

    try:
        r = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio = r.record(source)

        text = r.recognize_google(audio, language=language)
        return {"status": "success", "data": {"text": text, "confidence": 0.9}}
    except Exception as e:
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    try:
        params = json.loads(sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read())
        print(json.dumps(execute(params), ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)
