---
name: <汉字拼音> # e.g., sou
description: <一句话功能描述> # e.g., 执行网络搜索并返回结构化结果
tags: [tag1, tag2] # e.g., [search, web, crawler]
dependencies: [package1, package2] # e.g., [requests, beautifulsoup4]
---
# <汉字> (Character: <Pinyin>)

## 1. IO Contract (契约)

### Input Schema (JSON)
```json
{
  "param1": "string (description)",
  "param2": "integer (optional, default=10)"
}
```

### Output Schema (JSON)
```json
{
  "status": "success | error",
  "data": {
    "field1": "value1",
    "list_items": []
  }
}
```

### Failure Modes
- **NetworkError**: 当无法连接目标服务时返回。
- **ValidationError**: 当输入参数不符合 Schema 时返回。

## 2. Implementation (实现)

创建一个名为 `main.py` 的脚本，需包含依赖自检。

```python
import sys
import json

# --- Dependency Self-Check ---
try:
    import requests
except ImportError:
    print(json.dumps({"status": "error", "message": "Missing dependency: requests. Run: pip install requests"}))
    sys.exit(1)

# --- Core Logic ---
def execute(params):
    # TODO: Implement your logic here
    # Ensure statelessness and side-effect control
    return {"status": "success", "data": "result"}

if __name__ == "__main__":
    # Receive input via CLI argument (JSON string) or stdin
    try:
        input_str = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
        if not input_str.strip():
             raise ValueError("Empty input")
        params = json.loads(input_str)
        result = execute(params)
        print(json.dumps(result, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}), file=sys.stderr)
        sys.exit(1)
```

## 3. Tests & Examples (测试)

### Happy Path
```bash
python main.py '{"param1": "test"}'
# Expect: {"status": "success", ...}
```

### Edge Case
```bash
python main.py '{}'
# Expect: {"status": "error", "message": "..."}
```
