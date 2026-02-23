---
name: fa
description: 发布内容到平台（占位符）
tags: [publish, post, upload]
dependencies: []
五行: 水
---

# 发 (Character: fa)

## 1. IO Contract

### Input Schema
```json
{
  "content": "string (内容，必填)",
  "platform": "string (平台名称，必填)",
  "media": "string (可选，媒体文件路径)"
}
```

### Output Schema
```json
{
  "status": "success | error",
  "data": {
    "post_id": "string",
    "url": "string"
  }
}
```

## 2. Implementation
```python
import sys
import json

def execute(params):
    content = params.get("content", "").strip()
    platform = params.get("platform", "").strip()
    
    if not content or not platform:
        return {"status": "error", "message": "Content and platform required"}
    
    # 占位符实现
    return {"status": "error", "message": f"Platform '{platform}' not implemented yet. Please use platform-specific modules."}

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
python main.py '{"content": "Hello", "platform": "twitter"}'
```
