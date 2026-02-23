---
name: sou
description: 执行网络搜索并返回结构化结果
tags: [search, web, crawler, network]
dependencies: [requests, beautifulsoup4]
五行: 水
---

# 搜 (Character: sou)

## 1. IO Contract (契约)

### Input Schema (JSON)
```json
{
  "keywords": "string (搜索关键词，必填)",
  "limit": "integer (可选，返回结果数量，默认10)",
  "engine": "string (可选，搜索引擎，默认baidu)"
}
```

### Output Schema (JSON)
```json
{
  "status": "success | error",
  "data": {
    "results": [
      {
        "title": "string",
        "url": "string",
        "snippet": "string"
      }
    ],
    "count": "integer"
  }
}
```

### Failure Modes
- **NetworkError**: 当无法连接搜索引擎时返回
- **ValidationError**: 当关键词为空时返回

## 2. Implementation (实现)

```python
#!/usr/bin/env python3
"""
搜 (sou) - 网络搜索
执行网络搜索并返回结构化结果
"""
import sys
import json

# --- Dependency Self-Check ---
try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print(json.dumps({
        "status": "error", 
        "message": "Missing dependencies: requests, beautifulsoup4. Run: pip install requests beautifulsoup4"
    }))
    sys.exit(1)

# --- Core Logic ---
def search_baidu(keywords, limit=10):
    """百度搜索"""
    url = "https://www.baidu.com/s"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    params = {"wd": keywords, "rn": limit}
    
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        
        soup = BeautifulSoup(resp.text, 'html.parser')
        results = []
        
        for item in soup.select('.result')[:limit]:
            title_elem = item.select_one('h3 a')
            if title_elem:
                results.append({
                    "title": title_elem.get_text(),
                    "url": title_elem.get('href', ''),
                    "snippet": item.select_one('.c-abstract') or ""
                })
        
        return {"status": "success", "data": {"results": results, "count": len(results)}}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def search_google(keywords, limit=10):
    """Google搜索 (模拟)"""
    # 实际实现需要处理Google的反爬
    return {"status": "error", "message": "Google search not implemented yet"}

def execute(params):
    keywords = params.get("keywords", "").strip()
    if not keywords:
        return {"status": "error", "message": "Keywords cannot be empty"}
    
    limit = params.get("limit", 10)
    engine = params.get("engine", "baidu")
    
    if engine == "baidu":
        return search_baidu(keywords, limit)
    elif engine == "google":
        return search_google(keywords, limit)
    else:
        return {"status": "error", "message": f"Unknown engine: {engine}"}

if __name__ == "__main__":
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
python main.py '{"keywords": "Python 教程", "limit": 5}'
# Expect: {"status": "success", "data": {"results": [...], "count": 5}}
```

### Edge Case
```bash
python main.py '{"keywords": ""}'
# Expect: {"status": "error", "message": "Keywords cannot be empty"}
```
