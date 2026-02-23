---
name: du
description: 读取URL或本地文件内容
tags: [read, fetch, file, network]
dependencies: [requests, beautifulsoup4]
五行: 火
---

# 读 (Character: du)

## 1. IO Contract

### Input Schema
```json
{
  "source": "string (URL或文件路径，必填)",
  "type": "string (url|file，默认自动检测)"
}
```

### Output Schema
```json
{
  "status": "success | error",
  "data": {
    "content": "string",
    "type": "string",
    "length": "integer"
  }
}
```

### Failure Modes
- **NetworkError**: URL无法访问
- **FileNotFoundError**: 文件不存在
- **PermissionError**: 无读取权限

## 2. Implementation

```python
import sys
import json
import os

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print(json.dumps({"status": "error", "message": "Missing: pip install requests beautifulsoup4"}))
    sys.exit(1)

def read_url(source):
    try:
        resp = requests.get(source, timeout=10)
        resp.raise_for_status()
        return {"status": "success", "data": {"content": resp.text, "type": "url", "length": len(resp.text)}}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def read_file(source):
    try:
        if not os.path.exists(source):
            return {"status": "error", "message": f"File not found: {source}"}
        with open(source, 'r', encoding='utf-8') as f:
            content = f.read()
        return {"status": "success", "data": {"content": content, "type": "file", "length": len(content)}}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def execute(params):
    source = params.get("source", "").strip()
    if not source:
        return {"status": "error", "message": "Source cannot be empty"}
    
    source_type = params.get("type", "auto")
    if source_type == "auto":
        source_type = "url" if source.startswith(("http://", "https://")) else "file"
    
    if source_type == "url":
        return read_url(source)
    else:
        return read_file(source)

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
python main.py '{"source": "https://example.com"}'
python main.py '{"source": "test.txt", "type": "file"}'
```
