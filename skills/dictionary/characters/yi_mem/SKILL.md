---
name: yi_mem
description: 存入核心记忆（调用memory-core）
tags: [memory, store, RAG]
dependencies: []
五行: 土
---

# 忆 (Character: yi_mem)

## 1. IO Contract

### Input Schema
```json
{
  "content": "string (要记忆的内容，必填)",
  "tags": ["string"] (可选，标签列表)",
  "query": "string (可选，检索关键词)"
}
```

### Output Schema
```json
{
  "status": "success | error",
  "data": {
    "stored": "boolean",
    "retrieved": []
  }
}
```

## 2. Implementation
```python
import sys
import json
import subprocess

def execute(params):
    content = params.get("content", "").strip()
    query = params.get("query", "").strip()
    tags = params.get("tags", [])
    
    # 如果有query，先检索
    if query:
        cmd = [
            "python", "C:/Users/Administrator/.config/opencode/skills/memory-core/memory_core.py",
            "--action", "retrieve",
            "--query", query
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return {"status": "success", "data": {"query": query, "results": result.stdout}}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    # 否则存储
    if not content:
        return {"status": "error", "message": "Content required"}
    
    cmd = [
        "python", "C:/Users/Administrator/.config/opencode/skills/memory-core/memory_core.py",
        "--action", "context",
        "--content", content
    ]
    if tags:
        cmd.extend(["--tags", ",".join(tags)])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return {"status": "success", "data": {"stored": True, "content": content[:100]}}
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
python main.py '{"content": "重要信息：项目使用FastAPI"}'
python main.py '{"query": "FastAPI"}'
```
