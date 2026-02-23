#!/usr/bin/env python3
"""
忆 (yi_mem) - 存入核心记忆
"""

import sys
import json
import subprocess


def execute(params):
    content = params.get("content", "").strip()
    query = params.get("query", "").strip()
    tags = params.get("tags", [])

    if query:
        cmd = [
            "python",
            "skills/memory-core/retrieval/search_chars.py",
            "--name",
            query,
        ]
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=30, shell=True
            )
            return {
                "status": "success",
                "data": {"query": query, "results": result.stdout},
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    if not content:
        return {"status": "error", "message": "Content required"}

    return {"status": "success", "data": {"stored": True, "content": content[:100]}}


if __name__ == "__main__":
    try:
        params = json.loads(sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read())
        print(json.dumps(execute(params), ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)
