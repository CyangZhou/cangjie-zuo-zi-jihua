#!/usr/bin/env python3
"""
读 (du) - 读取URL或本地文件（纯Python）
"""

import sys
import json
import os
from urllib.request import urlopen
from urllib.error import URLError


def read_url(source):
    try:
        with urlopen(source, timeout=10) as resp:
            content = resp.read().decode("utf-8", errors="ignore")
        return {
            "status": "success",
            "data": {"content": content, "type": "url", "length": len(content)},
        }
    except URLError as e:
        return {"status": "error", "message": f"Network error: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def read_file(source):
    try:
        if not os.path.exists(source):
            return {"status": "error", "message": f"File not found: {source}"}
        with open(source, "r", encoding="utf-8") as f:
            content = f.read()
        return {
            "status": "success",
            "data": {"content": content, "type": "file", "length": len(content)},
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def execute(params):
    source = params.get("source", "").strip()
    if not source:
        return {"status": "error", "message": "Source cannot be empty"}

    source_type = params.get("type", "auto")
    if source_type == "auto":
        source_type = "url" if source.startswith(("http://", "https://")) else "file"

    if source_type == "url":
        return read_url(source)
    else:
        return read_file(source)


if __name__ == "__main__":
    try:
        params = json.loads(sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read())
        print(json.dumps(execute(params), ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)
