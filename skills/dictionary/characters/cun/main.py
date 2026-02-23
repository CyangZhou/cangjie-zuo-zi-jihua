#!/usr/bin/env python3
"""
存 (cun) - 保存内容到文件
"""

import sys
import json
import os


def execute(params):
    content = params.get("content", "")
    path = params.get("path", "").strip()

    if not path:
        return {"status": "error", "message": "Path cannot be empty"}

    mode = params.get("mode", "write")

    try:
        dir_path = os.path.dirname(path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        write_mode = "a" if mode == "append" else "w"
        with open(path, write_mode, encoding="utf-8") as f:
            bytes_written = f.write(content)
        return {
            "status": "success",
            "data": {"path": path, "bytes_written": bytes_written},
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    try:
        params = json.loads(sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read())
        print(json.dumps(execute(params), ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)
