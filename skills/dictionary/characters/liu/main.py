#!/usr/bin/env python3
"""
流 (liu) - 数据流管道
"""

import sys
import json
import os


def execute(params):
    source = params.get("source", "stdin")
    target = params.get("target", "stdout")

    try:
        if source == "stdin":
            data = sys.stdin.read()
        elif source.startswith("file:"):
            path = source[5:]
            with open(path, "r", encoding="utf-8") as f:
                data = f.read()
        else:
            return {"status": "error", "message": "Unsupported source"}

        if target == "stdout":
            print(data)
            return {
                "status": "success",
                "data": {"transferred": True, "bytes": len(data)},
            }
        elif target.startswith("file:"):
            path = target[5:]
            dir_path = os.path.dirname(path)
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(data)
            return {
                "status": "success",
                "data": {"transferred": True, "bytes": len(data), "path": path},
            }
        else:
            return {"status": "error", "message": "Unsupported target"}

    except Exception as e:
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    try:
        params = json.loads(sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read())
        print(json.dumps(execute(params), ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)
