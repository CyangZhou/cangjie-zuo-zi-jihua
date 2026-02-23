---
name: ting
description: 语音识别 (STT)
tags: [speech, audio, recognition, stt]
dependencies: [speechrecognition]
五行: 水
---

# 听 (Character: ting)

## 1. IO Contract

### Input Schema
```json
{
  "audio": "string (音频文件路径，必填)",
  "language": "string (可选，默认zh-CN)"
}
```

### Output Schema
```json
{
  "status": "success | error",
  "data": {
    "text": "string",
    "confidence": "number"
  }
}
```

## 2. Implementation
```python
import sys
import json

try:
    import speech_recognition as sr
except ImportError:
    print(json.dumps({"status": "error", "message": "Missing: pip install SpeechRecognition"}))
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
```

## 3. Tests
```bash
python main.py '{"audio": "recording.wav"}'
```
