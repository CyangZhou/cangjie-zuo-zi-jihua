#!/usr/bin/env python3
"""
取 (qu) - 纯Python下载（urllib内置库）
"""

import sys
import json
import os
from urllib.request import urlretrieve
from urllib.error import URLError


def execute(params):
    url = params.get("url", "").strip()
    output = params.get("output", "").strip()

    if not url or not output:
        return {"status": "error", "message": "URL and output required"}

    try:
        dir_path = os.path.dirname(output)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)

        urlretrieve(url, output)
        size = os.path.getsize(output)

        return {"status": "success", "data": {"path": output, "size": size}}
    except URLError as e:
        return {"status": "error", "message": f"Network error: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    try:
        params = json.loads(sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read())
        print(json.dumps(execute(params), ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)
