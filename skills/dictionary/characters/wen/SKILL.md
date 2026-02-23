---
name: wen
description: 纯Python模板问答
tags: [qa, template, question]
dependencies: []
五行: 水
---

# 问 (Character: wen)

## 1. IO Contract

### Input Schema
```json
{
  "question": "string (问题关键字，必填)",
  "type": "string (模板类型：what/who/where/when/why/how)"
}
```

### Output Schema
```json
{
  "status": "success | error",
  "data": {
    "answer": "string"
  }
}
```

## 2. Implementation
```python
import sys
import json
import random

QA_TEMPLATES = {
    "what": {
        "python": "Python是一种高级编程语言，简洁易读。",
        "ai": "AI是人工智能，使机器具有人类智能。",
        "default": "这是一个关于\"是什么\"的问题。"
    },
    "who": {
        "python": "Python由Guido van Rossum创建。",
        "default": "这是关于\"是谁\"的问题。"
    },
    "where": {
        "python": "Python可以运行在Windows、Linux、Mac等系统上。",
        "default": "这是关于\"在哪里\"的问题。"
    },
    "when": {
        "python": "Python首次发布于1991年。",
        "default": "这是关于\"什么时候\"的问题。"
    },
    "why": {
        "python": "因为它简洁易学，生态丰富。",
        "default": "这是关于\"为什么\"的问题。"
    },
    "how": {
        "python": "可以通过pip安装：pip install python",
        "default": "这是关于\"怎么做\"的问题。"
    }
}

def execute(params):
    question = params.get("question", "").strip().lower()
    qtype = params.get("type", "default")
    
    if not question:
        return {"status": "error", "message": "Question required"}
    
    # 简单关键词匹配
    keyword = "default"
    for key in QA_TEMPLATES.get(qtype, QA_TEMPLATES["what"]):
        if key in question:
            keyword = key
            break
    
    answer = QA_TEMPLATES.get(qtype, QA_TEMPLATES["what"]).get(keyword, "抱歉，我只能回答模板问题。")
    
    return {"status": "success", "data": {"answer": answer}}

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
python main.py '{"question": "什么是Python", "type": "what"}'
python main.py '{"question": "谁创造了Python", "type": "who"}'
```
