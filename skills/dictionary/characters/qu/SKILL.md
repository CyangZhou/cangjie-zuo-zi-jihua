---
name: qu
description: 纯Python下载（urllib内置库）
tags: [download, fetch, urllib]
dependencies: []
五行: 水
---

# 取 (Character: qu)

## 1. IO Contract

### Input Schema
```json
{
  "url": "string (资源URL，必填)",
  "output": "string (输出路径，必填)"
}
```

### Output Schema
```json
{
  "status": "success | error",
  "data": {
    "path": "string",
    "size": "integer"
  }
}
```

## 2. Implementation
```python
import sys
import json
import os
from urllib.request import urlretrieve, urlopen
from urllib.error import URLError

def execute(params):
    url = params.get("url", "").strip()
    output = params.get("output", "").strip()
    
    if not url or not output:
        return {"status": "error", "message": "URL and output required"}
    
    try:
        # 下载文件
        dir_path = os.path.dirname(output)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        
        urlretrieve(url, output)
        size = os.path.getsize(output)
        
        return {"status": "success", "data": {"path": output, "size": size}}
    except URLError as e:
        return {"status": "error", "message": f"Network error: {str(e)}"}
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
python main.py '{"url": "https://example.com/file.txt", "output": "file.txt"}'
```
