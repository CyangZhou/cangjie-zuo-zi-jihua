---
name: bi
description: 对比分析两个或多个对象
tags: [compare, analysis, diff]
dependencies: [difflib]
五行: 火
---

# 比 (Character: bi)

## 1. IO Contract

### Input Schema
```json
{
  "items": ["string"] (要对比的项列表，必填),
  "mode": "string (可选，text/json/list，默认text)"
}
```

### Output Schema
```json
{
  "status": "success | error",
  "data": {
    "comparison": "string",
    "similarities": [],
    "differences": []
  }
}
```

## 2. Implementation
```python
import sys
import json
import difflib

def execute(params):
    items = params.get("items", [])
    if len(items) < 2:
        return {"status": "error", "message": "At least 2 items required"}
    
    mode = params.get("mode", "text")
    
    if mode == "text" and len(items) == 2:
        diff = list(difflib.unified_diff(items[0].splitlines(), items[1].splitlines(), lineterm=''))
        comparison = '\n'.join(diff) if diff else "No differences found"
        return {"status": "success", "data": {"comparison": comparison, "items": items}}
    
    # 列表模式
    similarities = []
    differences = []
    for i in range(len(items)):
        for j in range(i+1, len(items)):
            sim = difflib.SequenceMatcher(None, str(items[i]), str(items[j])).ratio()
            if sim > 0.5:
                similarities.append({"a": items[i], "b": items[j], "ratio": sim})
            else:
                differences.append({"a": items[i], "b": items[j], "ratio": sim})
    
    return {"status": "success", "data": {"comparison": "", "similarities": similarities, "differences": differences}}

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
python main.py '{"items": ["方案A", "方案B"], "mode": "text"}'
```
