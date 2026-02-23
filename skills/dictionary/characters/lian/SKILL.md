---
name: lian
description: 纯Python文本摘要/关键词提取
tags: [summarize, extract, keyword]
dependencies: []
五行: 火
---

# 炼 (Character: lian)

## 1. IO Contract

### Input Schema
```json
{
  "text": "string (要提炼的文本，必填)",
  "mode": "string (模式：keywords/summary/first/count)",
  "count": "integer (关键词数量，默认5)"
}
```

### Output Schema
```json
{
  "status": "success | error",
  "data": {
    "result": "string 或 array"
  }
}
```

## 2. Implementation
```python
import sys
import json
import re
from collections import Counter

STOPWORDS = set(['的', '了', '是', '在', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这', 'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'dare', 'ought', 'used', 'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'as', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'between', 'under', 'again', 'further', 'then', 'once'])

def extract_keywords(text, count=5):
    # 分词
    words = re.findall(r'[\w]{2,}', text.lower())
    # 过滤停用词
    words = [w for w in words if w not in STOPWORDS]
    # 统计频率
    counter = Counter(words)
    # 返回Top N
    return [word for word, _ in counter.most_common(count)]

def execute(params):
    text = params.get("text", "").strip()
    if not text:
        return {"status": "error", "message": "Text required"}
    
    mode = params.get("mode", "keywords")
    count = params.get("count", 5)
    
    if mode == "keywords":
        result = extract_keywords(text, count)
    elif mode == "first":
        sentences = re.split(r'[。！？\n]', text)
        result = sentences[0] if sentences else text[:100]
    elif mode == "summary":
        sentences = [s.strip() for s in re.split(r'[。！？\n]', text) if s.strip()]
        result = "。".join(sentences[:3]) if sentences else text[:100]
    elif mode == "count":
        words = re.findall(r'[\w]+', text)
        result = {"chars": len(text), "words": len(words), "lines": len(text.split('\n'))}
    else:
        return {"status": "error", "message": f"Unknown mode: {mode}"}
    
    return {"status": "success", "data": {"result": result}}

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
python main.py '{"text": "Python是一种编程语言。Python简洁易读。Python生态丰富。", "mode": "keywords"}'
python main.py '{"text": "第一句。第二句。第三句。", "mode": "first"}'
```
