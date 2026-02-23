#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
运 (yun) - 代码执行技能
真正运行生成的代码并返回结果
"""

import sys
import json
import subprocess
import tempfile
import os


def run_code(code, language="python"):
    """运行代码并返回结果"""
    if language != "python":
        return {"status": "error", "message": f"Unsupported language: {language}"}

    # 创建临时文件
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, encoding="utf-8"
    ) as f:
        f.write(code)
        temp_file = f.name

    try:
        # 运行代码
        result = subprocess.run(
            [sys.executable, temp_file],
            capture_output=True,
            timeout=30,
            encoding="utf-8",
            errors="replace",
        )

        output = result.stdout
        error = result.stderr

        if result.returncode == 0:
            return {
                "status": "success",
                "data": {"output": output or "(无输出)", "returncode": 0},
            }
        else:
            return {
                "status": "error",
                "data": {
                    "output": output,
                    "error": error,
                    "returncode": result.returncode,
                },
            }
    except subprocess.TimeoutExpired:
        return {"status": "error", "message": "Timeout"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        # 清理临时文件
        try:
            os.unlink(temp_file)
        except:
            pass


def execute(params):
    code = params.get("code", "")
    language = params.get("language", "python")

    if not code:
        return {"status": "error", "message": "Code required"}

    return run_code(code, language)


if __name__ == "__main__":
    try:
        input_str = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
        if not input_str.strip():
            raise ValueError("Empty input")
        params = json.loads(input_str)
        result = execute(params)
        print(json.dumps(result, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}), file=sys.stderr)
        sys.exit(1)
