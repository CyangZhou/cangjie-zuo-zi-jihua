#!/usr/bin/env python3
"""
译 (yi) - 纯Python文本转换
"""

import sys
import json


def execute(params):
    text = params.get("text", "").strip()
    if not text:
        return {"status": "error", "message": "Text required"}

    mode = params.get("mode", "reverse")

    if mode == "reverse":
        result = text[::-1]
    elif mode == "upper":
        result = text.upper()
    elif mode == "lower":
        result = text.lower()
    elif mode == "capitalize":
        result = text.capitalize()
    elif mode == "title":
        result = text.title()
    elif mode == "swap":
        result = text.swapcase()
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
