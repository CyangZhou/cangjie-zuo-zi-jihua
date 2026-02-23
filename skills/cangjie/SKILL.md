---
name: cangjie
description: 仓颉造字 - 只要会中文就能编程。让AI理解中文需求并执行任务。
tags: [编程, 执行, 中文, 自动化]
dependencies: []
五行: 混沌
---

# 仓颉 (cangjie)

## 1. IO Contract

### Input Schema
```json
{
  "requirement": "string (中文需求描述，必填)",
  "options": {
    "remember": "boolean (是否记忆这次执行，默认true)",
    "verbose": "boolean (是否详细输出，默认false)"
  }
}
```

### Output Schema
```json
{
  "status": "success | error",
  "result": "any (执行结果)",
  "display": "string (可视化展示)",
  "explanation": "string (中文解释)",
  "guide": "object (操作指引)"
}
```

### 支持的需求模式
| 模式 | 示例 | 执行的技能链 |
|------|------|-------------|
| 搜索 | 搜索Python教程 | sou |
| 写作 | 写一个计算器 | xie |
| 读取 | 读取 https://x.com | du |
| 保存 | 保存内容到文件 | cun |
| 写+运行 | 写一个HelloWorld并运行 | xie → yun |
| 搜索+保存 | 搜索AI新闻并保存 | sou → cun |

## 2. Implementation

```python
import sys
import json
import subprocess
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SKILLS = {
    "sou": os.path.join(BASE_DIR, "dictionary", "characters", "sou", "main.py"),
    "xie": os.path.join(BASE_DIR, "dictionary", "characters", "xie", "main.py"),
    "du": os.path.join(BASE_DIR, "dictionary", "characters", "du", "main.py"),
    "cun": os.path.join(BASE_DIR, "dictionary", "characters", "cun", "main.py"),
    "yun": os.path.join(BASE_DIR, "dictionary", "characters", "yun", "main.py"),
    "dong": os.path.join(BASE_DIR, "dictionary", "characters", "dong", "main.py"),
    "ce": os.path.join(BASE_DIR, "dictionary", "characters", "ce", "main.py"),
    "xing": os.path.join(BASE_DIR, "dictionary", "characters", "xing", "main.py"),
    "yan": os.path.join(BASE_DIR, "dictionary", "characters", "yan", "main.py"),
    "xiu": os.path.join(BASE_DIR, "dictionary", "characters", "xiu", "main.py"),
}

def run_skill(name, params):
    path = SKILLS.get(name)
    if not path or not os.path.exists(path):
        return {"status": "error", "message": f"Skill not found: {name}"}
    
    try:
        result = subprocess.run(
            [sys.executable, path],
            input=json.dumps(params, ensure_ascii=False).encode("utf-8"),
            capture_output=True,
            timeout=60,
        )
        return json.loads(result.stdout.decode("utf-8"))
    except Exception as e:
        return {"status": "error", "message": str(e)}

def detect_chain(requirement):
    """检测技能链"""
    req = requirement
    if "搜" in req or "找" in req:
        if "保存" in req or "存" in req:
            return ["sou", "cun"]
        return ["sou"]
    if "写" in req or "生成" in req or "创建" in req:
        if "运行" in req or "跑" in req:
            return ["xie", "yun"]
        if "保存" in req:
            return ["xie", "cun"]
        return ["xie"]
    if "读" in req or "看" in req:
        return ["du"]
    if "保存" in req or "存" in req:
        return ["cun"]
    return ["sou"]  # 默认搜索

def execute(params):
    requirement = params.get("requirement", "").strip()
    if not requirement:
        return {"status": "error", "message": "需求不能为空"}
    
    # 检测技能链
    chain = detect_chain(requirement)
    
    # 依次执行
    context = {}
    for skill in chain:
        if skill == "sou":
            result = run_skill("sou", {"keywords": requirement})
        elif skill == "xie":
            result = run_skill("xie", {"description": requirement})
        elif skill == "du":
            # 提取URL
            import re
            urls = re.findall(r'https?://[^\s]+', requirement)
            source = urls[0] if urls else requirement
            result = run_skill("du", {"source": source})
        elif skill == "cun":
            content = context.get("data", {}).get("result", requirement)
            result = run_skill("cun", {"content": str(content), "path": "output.txt"})
        elif skill == "yun":
            code = context.get("data", {}).get("result", "print('Hello')")
            result = run_skill("yun", {"code": code, "language": "python"})
        else:
            continue
        
        if result.get("status") == "error":
            return result
        context = result.get("data", {})
    
    return {
        "status": "success",
        "result": context,
        "display": str(context)[:200],
        "explanation": f"已完成：{' + '.join(chain)}",
        "guide": {"next": ["查看结果", "继续下一个"]}
    }

if __name__ == "__main__":
    try:
        params = json.loads(sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read())
        print(json.dumps(execute(params), ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))
```

## 3. Tests

```bash
# 搜索
python main.py '{"requirement": "搜索Python教程"}'

# 写作+运行
python main.py '{"requirement": "写一个HelloWorld并运行"}'

# 读取
python main.py '{"requirement": "读取 https://example.com"}'
```

## 4. 使用方式

作为我的内置技能，你可以直接说：
- "搜一下Python教程"
- "写个计算器并运行"
- "看看这个网页 https://x.com"

我理解后会自动执行相应的技能链。
