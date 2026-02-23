#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""画 (hua) - 简单图形生成"""
import sys
import json

def execute(params):
    text = params.get("text", "Hello")
    return {"status": "success", "data": {"result": f"[图形]: {text}"}}

if __name__ == "__main__":
    try:
        params = json.loads(sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read())
        print(json.dumps(execute(params), ensure_ascii=False))
    except: print(json.dumps({"status": "error", "message": "Failed"}))
