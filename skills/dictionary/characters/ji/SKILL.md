---
name: ji
description: 记录日志到文件
tags: [log, record, write]
dependencies: []
五行: 土
---

# 记 (Character: ji)

## 1. IO Contract

### Input Schema
```json
{
  "message": "string (日志内容，必填)",
  "file": "string (可选，日志文件路径，默认logs.txt)",
  "level": "string (可选，info/warning/error)"
}
```

### Output Schema
```json
{
  "status": "success | error",
  "data": {
    "logged": "boolean",
    "file": "string"
  }
}
```

## 2. Implementation
```python
import sys
import json
import os
from datetime import datetime

def execute(params):
    message = params.get("message", "").strip()
    if not message:
        return {"status": "error", "message": "Message cannot be empty"}
    
    log_file = params.get("file", "logs.txt")
    level = params.get("level", "info")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [{level.upper()}] {message}\n"
    
    try:
        dir_path = os.path.dirname(log_file)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_line)
        
        return {"status": "success", "data": {"logged": True, "file": log_file}}
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
python main.py '{"message": "Task completed", "level": "info"}'
```
