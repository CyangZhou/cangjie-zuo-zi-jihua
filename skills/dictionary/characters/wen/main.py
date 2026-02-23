#!/usr/bin/env python3
"""
问 (wen) - 纯Python模板问答
"""

import sys
import json

QA_TEMPLATES = {
    "what": {
        "python": "Python是一种高级编程语言，简洁易读。",
        "ai": "AI是人工智能。",
        "default": "这是关于是什么的问题。",
    },
    "who": {
        "python": "Python由Guido van Rossum创建。",
        "default": "这是关于是谁的问题。",
    },
    "where": {
        "python": "Python可运行在Windows、Linux、Mac等系统。",
        "default": "这是关于哪里的问题。",
    },
    "when": {
        "python": "Python首次发布于1991年。",
        "default": "这是关于什么时候的问题。",
    },
    "why": {
        "python": "因为它简洁易学，生态丰富。",
        "default": "这是关于为什么的问题。",
    },
    "how": {"python": "可以通过pip安装。", "default": "这是关于怎么做的问题。"},
}


def execute(params):
    question = params.get("question", "").strip().lower()
    qtype = params.get("type", "what")

    if not question:
        return {"status": "error", "message": "Question required"}

    keyword = "default"
    for key in QA_TEMPLATES.get(qtype, QA_TEMPLATES["what"]):
        if key in question:
            keyword = key
            break

    answer = QA_TEMPLATES.get(qtype, QA_TEMPLATES["what"]).get(
        keyword, "抱歉，我只能回答模板问题。"
    )
    return {"status": "success", "data": {"answer": answer}}


if __name__ == "__main__":
    try:
        params = json.loads(sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read())
        print(json.dumps(execute(params), ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)
