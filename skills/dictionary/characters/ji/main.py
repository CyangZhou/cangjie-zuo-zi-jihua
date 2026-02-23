#!/usr/bin/env python3
"""
记 (ji) - 记录日志
"""

import sys
import json
import os
from datetime import datetime


def execute(params):
    message = params.get("message", "").strip()
    if not message:
        return {"status": "error", "message": "Message cannot be empty"}

    log_file = params.get("file", "logs.txt")
    level = params.get("level", "info")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [{level.upper()}] {message}\n"

    try:
        dir_path = os.path.dirname(log_file)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)

        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_line)

        return {"status": "success", "data": {"logged": True, "file": log_file}}
    except Exception as e:
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    try:
        params = json.loads(sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read())
        print(json.dumps(execute(params), ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)
