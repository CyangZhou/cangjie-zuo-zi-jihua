#!/usr/bin/env python3
"""
改 (gai) - 纯Python文本替换
"""

import sys
import json
import re


def execute(params):
    text = params.get("text", "")
    find = params.get("find", "")
    replace = params.get("replace", "")
    use_regex = params.get("regex", False)

    if not text:
        return {"status": "error", "message": "Text required"}
    if not find:
        return {"status": "error", "message": "Find string required"}

    try:
        if use_regex:
            result = re.sub(find, replace, text)
        else:
            result = text.replace(find, replace)
        return {"status": "success", "data": {"result": result}}
    except Exception as e:
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    try:
        params = json.loads(sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read())
        print(json.dumps(execute(params), ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)
