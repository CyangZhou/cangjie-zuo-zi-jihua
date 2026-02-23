---
name: pei
description: 纯Python时间轴计算（生成字幕时间）
tags: [timeline, subtitle, time]
dependencies: []
五行: 火
---

# 配 (Character: pei)

## 1. IO Contract

### Input Schema
```json
{
  "text": "string (字幕文本，每行一句)",
  "duration": "number (每句时长秒，默认3)",
  "format": "string (srt/vtt，默认srt)"
}
```

### Output Schema
```json
{
  "status": "success | error",
  "data": {
    "timeline": "string (时间轴)"
  }
}
```

## 2. Implementation
```python
import sys
import json

def format_srt_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def format_vtt_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"

def execute(params):
    text = params.get("text", "").strip()
    if not text:
        return {"status": "error", "message": "Text required"}
    
    duration = params.get("duration", 3)
    format_type = params.get("format", "srt")
    
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    timeline = ""
    
    for i, line in enumerate(lines, 1):
        start = (i - 1) * duration
        end = i * duration
        
        if format_type == "srt":
            timeline += f"{i}\n"
            timeline += f"{format_srt_time(start)} --> {format_srt_time(end)}\n"
        else:  # vtt
            timeline += f"{format_vtt_time(start)} --> {format_vtt_time(end)}\n"
        
        timeline += f"{line}\n\n"
    
    return {"status": "success", "data": {"timeline": timeline}}

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
python main.py '{"text": "第一句\n第二句\n第三句", "duration": 2}'
```
