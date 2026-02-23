---
name: gai
description: 纯Python文本替换/正则处理
tags: [replace, regex, text]
dependencies: []
五行: 火
---

# 改 (Character: gai)

## 1. IO Contract

### Input Schema
```json
{
  "text": "string (要修改的文本，必填)",
  "find": "string (要查找的内容)",
  "replace": "string (替换后的内容)",
  "regex": "boolean (是否使用正则，默认false)"
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
import re

def execute(params):
    text = params.get("text", "")
    find = params.get("find", "")
    replace = params.get("replace", "")
    use_regex = params.get("regex", False)
    
    if not text:
        return {"status": "error", "message": "Text required"}
    
    if not find:
        return {"status": "error", "message": "Find string required"}
    
    try:
        if use_regex:
            result = re.sub(find, replace, text)
        else:
            result = text.replace(find, replace)
        return {"status": "success", "data": {"result": result}}
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
python main.py '{"text": "hello world", "find": "world", "replace": "python"}'
python main.py '{"text": "abc123", "find": "[0-9]+", "replace": "X", "regex": true}'
```
