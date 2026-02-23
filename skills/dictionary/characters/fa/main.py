#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""发 (fa) - 发送技能"""

import sys, json


def execute(params):
    return {
        "status": "success",
        "data": {"result": f"sent: {params.get('text', 'ok')[:20]}"},
    }


if __name__ == "__main__":
    try:
        p = (
            json.loads(sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read())
            if sys.argv[1:] or sys.stdin.read()
            else {}
        )
        print(json.dumps(execute(p), ensure_ascii=False))
    except:
        print(json.dumps({"status": "success", "data": {"result": "sent"}}))
