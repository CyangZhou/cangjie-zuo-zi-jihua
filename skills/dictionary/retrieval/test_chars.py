#!/usr/bin/env python3
"""
单字技能检测工具
检测所有单字技能是否可用
"""

import os
import sys
import json
import subprocess

# 修复 Windows 中文编码
if sys.platform == "win32":
    import io

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

# 获取字符目录 - 向上两级到 dictionary
chars_dir = os.path.join(os.path.dirname(__file__), "..", "characters")

# 测试用例
TEST_CASES = {
    "sou": {"keywords": "test"},
    "du": {"source": "https://example.com"},
    "xie": {"template": "list", "content": {"items": ["a", "b"]}},
    "cun": {"content": "test", "path": "test.txt"},
    "yi": {"text": "hello", "mode": "upper"},
    "gai": {"text": "hello world", "find": "world", "replace": "python"},
    "pei": {"text": "第一句\n第二句", "duration": 2},
    "mu": {"text": "第一句\n第二句"},
    "jian": {"input": "test.mp4", "output": "test.mp4"},
    "hua": {"subject": "一只猫", "style": "anime"},
    "ting": {"audio": "test.wav"},
    "bi": {"items": ["a", "b"]},
    "qu": {"url": "https://example.com/", "output": "test.html"},
    "fa": {"content": "test", "platform": "twitter"},
    "ji": {"message": "test", "level": "info"},
    "kong": {"action": "screenshot", "params": {"output": "test.png"}},
    "liu": {"source": "stdin", "target": "stdout"},
    "wen": {"question": "什么是Python", "type": "what"},
    "yi_mem": {"content": "test"},
    "lian": {"text": "Python编程语言Python简洁", "mode": "keywords"},
}


def test_char(char_name):
    """测试单个字符"""
    char_dir = os.path.join(chars_dir, char_name)
    main_py = os.path.join(char_dir, "main.py")

    if not os.path.exists(main_py):
        return {"status": "not_found", "message": "main.py not found"}

    test_input = TEST_CASES.get(char_name, {})

    try:
        result = subprocess.run(
            [sys.executable, main_py, json.dumps(test_input)],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=chars_dir,
        )

        output = result.stdout.strip()
        if not output:
            output = result.stderr.strip()

        try:
            parsed = json.loads(output)
            return parsed
        except:
            return {"status": "parse_error", "output": output[:200]}

    except subprocess.TimeoutExpired:
        return {"status": "timeout", "message": "Execution timeout"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def main():
    print("=" * 60)
    print("单字技能检测报告")
    print("=" * 60)

    if not os.path.exists(chars_dir):
        print(f"Error: 目录不存在: {chars_dir}")
        return

    chars = sorted(
        [
            d
            for d in os.listdir(chars_dir)
            if os.path.isdir(os.path.join(chars_dir, d)) and d != "__pycache__"
        ]
    )

    results = {"success": [], "error": [], "not_found": []}

    for char in chars:
        result = test_char(char)
        status = result.get("status", "unknown")

        if status in ["success", "not_found"]:
            results[status].append(char)
        else:
            results["error"].append((char, result))

    print(f"\n总计: {len(chars)} 个单字\n")

    print("✅ 可用:")
    for char in results["success"]:
        print(f"  - {char}")

    print("\n⚠️ 需要配置/依赖:")
    for char, result in results["error"]:
        msg = result.get("message", result.get("status", "unknown"))[:50]
        print(f"  - {char}: {msg}")

    print("\n❌ 未找到:")
    for char in results["not_found"]:
        print(f"  - {char}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
