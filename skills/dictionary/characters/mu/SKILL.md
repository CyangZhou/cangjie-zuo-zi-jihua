---
name: mu
description: 生成字幕文件
tags: [subtitle, caption, video]
dependencies: []
五行: 火
---

# 幕 (Character: mu)

## 1. IO Contract

### Input Schema
```json
{
  "text": "string (字幕文本，必填)",
  "format": "string (可选，srt/vtt，默认srt)",
  "duration": "number (可选，每段时长秒，默认3)"
}
```

### Output Schema
```json
{
  "status": "success | error",
  "data": {
    "subtitle": "string",
    "format": "string"
  }
}
```

## 2. Implementation
```python
import sys
import json

def execute(params):
    text = params.get("text", "").strip()
    if not text:
        return {"status": "error", "message": "Text cannot be empty"}
    
    format_type = params.get("format", "srt")
    duration = params.get("duration", 3)
    
    # 按句子分割
    sentences = [s.strip() for s in text.split('\n') if s.strip()]
    
    subtitle = ""
    for i, sentence in enumerate(sentences, 1):
        start = (i-1) * duration
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
```

## 3. Tests
```bash
python main.py '{"text": "第一句\n第二句\n第三句"}'
```
