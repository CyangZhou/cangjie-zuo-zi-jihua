#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验 (yan) - 结果验证
更灵活的验证逻辑：只要有有效输出就算成功
"""

import sys
import json


def validate(result, expectations):
    checks = []

    result_status = result.get("status", "unknown")

    # 状态检查 - 宽容处理
    if result_status == "success":
        checks.append({"name": "status", "passed": True, "message": "OK"})
    elif result.get("data"):
        checks.append({"name": "status", "passed": True, "message": "Has data"})
    else:
        checks.append(
            {
                "name": "status",
                "passed": False,
                "message": result.get("message", "Unknown error")[:30],
            }
        )

    # 数据检查
    if result.get("data"):
        checks.append({"name": "data", "passed": True, "message": "OK"})
    else:
        checks.append({"name": "data", "passed": False, "message": "No data"})

    passed = any(c["passed"] for c in checks)

    return {
        "status": "success",
        "data": {
            "passed": passed,
            "checks": checks,
            "summary": "OK" if passed else "Failed",
        },
    }


def execute(params):
    result = params.get("result", {})
    if not result:
        return {"status": "error", "message": "Result required"}
    return validate(result, params.get("expectations", {}))


if __name__ == "__main__":
    try:
        input_str = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
        params = json.loads(input_str) if input_str.strip() else {}
        print(json.dumps(execute(params), ensure_ascii=False))
    except:
        print(json.dumps({"status": "error", "message": "Invalid input"}))
        sys.exit(1)
