---
name: dong
description: 理解中文需求描述，提取意图、实体和约束条件
tags: [intent, understanding, nlp, chinese]
dependencies: []
五行: 火
---

# 懂 (Character: dong)

## 1. IO Contract (契约)

### Input Schema (JSON)
```json
{
  "requirement": "string (用户的中文需求描述，必填)",
  "context": "object (可选，上下文信息)"
}
```

### Output Schema (JSON)
```json
{
  "status": "success | error",
  "data": {
    "intent": {
      "type": "string (意图类型: search|read|write|execute|analyze|create|modify|delete)",
      "confidence": "float (置信度 0-1)",
      "keywords": ["string", ...]
    },
    "entities": [
      {
        "name": "string (实体名)",
        "value": "string (实体值)",
        "type": "string (类型: file|url|text|command|function)"
      }
    ],
    "constraints": {
      "format": "string (输出格式要求)",
      "language": "string (语言要求)",
      "length": "string (长度要求)"
    },
    "action_plan": "string (建议的下一步动作)"
  }
}
```

### Failure Modes
- **EmptyInput**: 当需求描述为空时返回
- **InvalidFormat**: 当输入不是有效JSON时返回

## 2. Implementation (实现)

```python
#!/usr/bin/env python3
"""
懂 (dong) - 中文意图理解
理解中文需求描述，提取意图、实体和约束条件
"""
import sys
import json
import re

# --- Intent Patterns (意图模式) ---
INTENT_PATTERNS = {
    "search": [
        r"搜索", r"查找", r"找", r"查询", r"搜", r"获取",
        r"怎么", r"如何", r"怎样", r"什么", r"哪个", r"哪些"
    ],
    "read": [
        r"读取", r"打开", r"看", r"查看", r"显示", r"展示",
        r"内容", r"文件", r"文章", r"资料"
    ],
    "write": [
        r"写", r"创建", r"生成", r"制作", r"新增",
        r"添加", r"编辑", r"修改", r"更新"
    ],
    "execute": [
        r"运行", r"执行", r"跑", r"启动", r"开始",
        r"完成", r"实现", r"做", r"帮我"
    ],
    "analyze": [
        r"分析", r"统计", r"计算", r"比较", r"评估",
        r"检查", r"验证", r"测试"
    ],
    "create": [
        r"新建", r"开发", r"构建", r"编程", r"写代码"
    ],
    "modify": [
        r"改", r"修复", r"优化", r"改进", r"调整"
    ],
    "delete": [
        r"删除", r"移除", r"清除", r"去掉"
    ]
}

# --- Entity Patterns (实体模式) ---
ENTITY_PATTERNS = {
    "file": [
        r"[^\s]+\.(py|js|ts|md|txt|json|yaml|yml|xml|html|css)",
        r"文件[^\s]*"
    ],
    "url": [
        r"https?://[^\s]+",
        r"网站[^\s]*",
        r"链接[^\s]*"
    ],
    "command": [
        r"命令[^\s]*",
        r"指令[^\s]*",
        r"终端[^\s]*"
    ]
}

# --- Core Logic ---
def extract_intent(text):
    """提取意图类型"""
    scores = {}
    for intent, patterns in INTENT_PATTERNS.items():
        score = 0
        for pattern in patterns:
            if re.search(pattern, text):
                score += 1
        scores[intent] = score
    
    if max(scores.values()) == 0:
        return {"type": "execute", "confidence": 0.5, "keywords": []}
    
    best_intent = max(scores, key=scores.get)
    confidence = scores[best_intent] / (scores[best_intent] + 1)
    
    # 提取关键词
    keywords = []
    for pattern in INTENT_PATTERNS[best_intent]:
        matches = re.findall(pattern, text)
        keywords.extend(matches)
    
    return {"type": best_intent, "confidence": min(confidence + 0.3, 0.95), "keywords": list(set(keywords))}

def extract_entities(text):
    """提取实体"""
    entities = []
    
    # 提取文件路径
    file_pattern = r"([^\s]+\.(py|js|ts|md|txt|json|yaml|yml|xml|html|css))"
    for match in re.finditer(file_pattern, text):
        entities.append({
            "name": "file",
            "value": match.group(1),
            "type": "file"
        })
    
    # 提取URL
    url_pattern = r"(https?://[^\s]+)"
    for match in re.finditer(url_pattern, text):
        entities.append({
            "name": "url",
            "value": match.group(1),
            "type": "url"
        })
    
    return entities

def extract_constraints(text):
    """提取约束条件"""
    constraints = {}
    
    # 格式要求
    format_match = re.search(r"(json|yaml|xml|csv|markdown|html|python|javascript)", text, re.IGNORECASE)
    if format_match:
        constraints["format"] = format_match.group(1).lower()
    
    # 语言要求
    lang_match = re.search(r"(中文|英文|英文|双语)", text)
    if lang_match:
        constraints["language"] = lang_match.group(1)
    
    # 长度要求
    length_match = re.search(r"(简单|详细|简短|长|短|多少)", text)
    if length_match:
        constraints["length"] = length_match.group(1)
    
    return constraints

def generate_action_plan(intent, entities, constraints):
    """生成建议的下一步动作"""
    intent_to_action = {
        "search": "使用'搜'技能进行网络搜索",
        "read": "使用'读'技能读取指定内容",
        "write": "使用'写'技能生成内容",
        "execute": "分析需求，制定执行计划",
        "analyze": "使用'比'或'炼'技能进行分析",
        "create": "使用'创'技能或组合现有技能",
        "modify": "使用'改'技能进行修改",
        "delete": "使用'删'技能执行删除"
    }
    
    base_action = intent_to_action.get(intent, "需要进一步分析")
    
    if entities:
        entity_names = [e["type"] for e in entities]
        return f"{base_action}，涉及实体: {', '.join(entity_names)}"
    
    return base_action

def understand(text, context=None):
    """理解中文需求"""
    result = {
        "intent": extract_intent(text),
        "entities": extract_entities(text),
        "constraints": extract_constraints(text),
        "action_plan": ""
    }
    result["action_plan"] = generate_action_plan(
        result["intent"]["type"],
        result["entities"],
        result["constraints"]
    )
    
    return {"status": "success", "data": result}

def execute(params):
    requirement = params.get("requirement", "").strip()
    if not requirement:
        return {"status": "error", "message": "EmptyInput: requirement cannot be empty"}
    
    context = params.get("context", {})
    return understand(requirement, context)

# --- Entry Point ---
if __name__ == "__main__":
    try:
        input_str = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
        if not input_str.strip():
            raise ValueError("Empty input")
        params = json.loads(input_str)
        result = execute(params)
        print(json.dumps(result, ensure_ascii=False))
    except json.JSONDecodeError as e:
        print(json.dumps({"status": "error", "message": f"InvalidFormat: {str(e)}"}), file=sys.stderr)
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}), file=sys.stderr)
        sys.exit(1)
```

## 3. Tests & Examples (测试)

### Happy Path
```bash
python main.py '{"requirement": "帮我搜索Python教程"}'
# Expect: {"status": "success", "data": {"intent": {"type": "search", ...}, "entities": [], ...}}
```

### Complex Requirement
```bash
python main.py '{"requirement": "帮我写一个Python脚本，读取test.txt文件并统计字数"}'
# Expect: intent=read+write, entities=[file:test.txt], action_plan=...
```

### Edge Case
```bash
python main.py '{"requirement": ""}'
# Expect: {"status": "error", "message": "EmptyInput: requirement cannot be empty"}
```
