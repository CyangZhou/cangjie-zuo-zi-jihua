---
name: yi
description: 纯Python简单翻译（内置词典）
tags: [translate, dictionary]
dependencies: []
五行: 火
---

# 译 (Character: yi)

## 1. IO Contract

### Input Schema
```json
{
  "text": "string (要翻译的文本，必填)",
  "mode": "string (可选，reverse大小写反转/upper大写/lower小写/capitalize首字母大写)"
}
```

### Output Schema
```json
{
  "status": "success | error",
  "data": {
    "result": "string"
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
        return {"status": "error", "message": "Text required"}
    
    mode = params.get("mode", "reverse")
    
    if mode == "reverse":
        result = text[::-1]
    elif mode == "upper":
        result = text.upper()
    elif mode == "lower":
        result = text.lower()
    elif mode == "capitalize":
        result = text.capitalize()
    elif mode == "title":
        result = text.title()
    elif mode == "swap":
        result = text.swapcase()
    else:
        return {"status": "error", "message": f"Unknown mode: {mode}"}
    
    return {"status": "success", "data": {"result": result}}

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
python main.py '{"text": "hello", "mode": "upper"}'
python main.py '{"text": "ABC", "mode": "lower"}'
```
