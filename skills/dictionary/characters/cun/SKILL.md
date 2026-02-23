---
name: cun
description: 保存内容到文件
tags: [save, write, file, storage]
dependencies: []
五行: 土
---

# 存 (Character: cun)

## 1. IO Contract

### Input Schema
```json
{
  "content": "string (要保存的内容，必填)",
  "path": "string (文件路径，必填)",
  "mode": "string (可选，write/append，默认write)"
}
```

### Output Schema
```json
{
  "status": "success | error",
  "data": {
    "path": "string",
    "bytes_written": "integer"
  }
}
```

### Failure Modes
- **PermissionError**: 无写入权限
- **DirectoryNotFoundError**: 目录不存在

## 2. Implementation
```python
import sys
import json
import os

def execute(params):
    content = params.get("content", "")
    path = params.get("path", "").strip()
    
    if not path:
        return {"status": "error", "message": "Path cannot be empty"}
    
    mode = params.get("mode", "write")
    
    try:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        write_mode = "a" if mode == "append" else "w"
        with open(path, write_mode, encoding="utf-8") as f:
            bytes_written = f.write(content)
        return {"status": "success", "data": {"path": path, "bytes_written": bytes_written}}
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
python main.py '{"content": "Hello World", "path": "output.txt"}'
python main.py '{"content": "Appended", "path": "output.txt", "mode": "append"}'
```
