#!/usr/bin/env python3
"""
控 (kong) - 桌面控制
"""

import sys
import json
import os

try:
    import pyautogui
    from PIL import Image
except ImportError:
    print(
        json.dumps(
            {"status": "error", "message": "Missing: pip install pyautogui pillow"}
        )
    )
    sys.exit(1)


def execute(params):
    action = params.get("action", "").strip()
    if not action:
        return {"status": "error", "message": "Action required"}

    pyautogui.FAILSAFE = True

    if action == "screenshot":
        output = params.get("params", {}).get("output", "screenshot.png")
        img = pyautogui.screenshot()
        img.save(output)
        return {"status": "success", "data": {"path": output}}

    elif action == "click":
        x = params.get("params", {}).get("x", 0)
        y = params.get("params", {}).get("y", 0)
        pyautogui.click(x, y)
        return {"status": "success", "data": {"clicked": f"{x},{y}"}}

    elif action == "move":
        x = params.get("params", {}).get("x", 0)
        y = params.get("params", {}).get("y", 0)
        pyautogui.moveTo(x, y)
        return {"status": "success", "data": {"moved_to": f"{x},{y}"}}

    elif action == "type":
        text = params.get("params", {}).get("text", "")
        pyautogui.write(text)
        return {"status": "success", "data": {"typed": text}}

    else:
        return {"status": "error", "message": f"Unknown action: {action}"}


if __name__ == "__main__":
    try:
        params = json.loads(sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read())
        print(json.dumps(execute(params), ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)
