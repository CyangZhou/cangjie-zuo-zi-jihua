---
name: hua
description: 纯Python生成绘画Prompt描述
tags: [prompt, generate, describe]
dependencies: []
五行: 木
---

# 画 (Character: hua)

## 1. IO Contract

### Input Schema
```json
{
  "subject": "string (主体，必填)",
  "style": "string (风格：realistic/anime/pixel/cartoon/abstract)",
  "mood": "string (氛围：bright/dark/peaceful/energetic)",
  "extra": "string (额外描述)"
}
```

### Output Schema
```json
{
  "status": "success | error",
  "data": {
    "prompt": "string"
  }
}
```

## 2. Implementation
```python
import sys
import json

STYLES = {
    "realistic": "photorealistic, detailed, 8k, high resolution",
    "anime": "anime style, manga, vibrant colors",
    "pixel": "pixel art, 8-bit, retro game",
    "cartoon": "cartoon style, animated, fun",
    "abstract": "abstract art, geometric shapes, colorful",
    "watercolor": "watercolor painting, soft colors",
    "oil": "oil painting style, dramatic lighting"
}

MOODS = {
    "bright": "bright, sunny, vibrant",
    "dark": "dark, moody, dramatic shadows",
    "peaceful": "peaceful, calm, serene",
    "energetic": "energetic, dynamic, powerful",
    "mysterious": "mysterious, enigmatic, foggy",
    "warm": "warm, cozy, golden hour"
}

def execute(params):
    subject = params.get("subject", "").strip()
    if not subject:
        return {"status": "error", "message": "Subject required"}
    
    style = params.get("style", "realistic")
    mood = params.get("mood", "bright")
    extra = params.get("extra", "")
    
    prompt = f"{subject}"
    prompt += f", {STYLES.get(style, STYLES['realistic'])}"
    prompt += f", {MOODS.get(mood, MOODS['bright'])}"
    if extra:
        prompt += f", {extra}"
    prompt += ", beautiful, masterpiece"
    
    return {"status": "success", "data": {"prompt": prompt}}

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
python main.py '{"subject": "一只猫", "style": "anime", "mood": "peaceful"}'
```
