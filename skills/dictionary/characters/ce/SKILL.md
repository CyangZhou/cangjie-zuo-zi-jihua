---
name: ce
description: 根据需求分析制定执行计划，选择合适的技能组合
tags: [planning, strategy, workflow, coordinator]
dependencies: []
五行: 土
---

# 策 (Character: ce)

## 1. IO Contract (契约)

### Input Schema (JSON)
```json
{
  "intent": {
    "type": "string (意图类型: search|read|write|execute|analyze|create|modify|delete)",
    "confidence": "float",
    "keywords": ["string"]
  },
  "entities": [
    {
      "name": "string",
      "value": "string",
      "type": "string (file|url|text|command|function)"
    }
  ],
  "constraints": {
    "format": "string",
    "language": "string",
    "length": "string"
  }
}
```

### Output Schema (JSON)
```json
{
  "status": "success | error",
  "data": {
    "plan": [
      {
        "step": "integer (步骤序号)",
        "skill": "string (技能名)",
        "input": "object (输入参数)",
        "reason": "string (为什么选择这个技能)"
      }
    ],
    "estimated_steps": "integer",
    "fallback": "string (备选计划说明)"
  }
}
```

### Failure Modes
- **InvalidInput**: 当输入格式不正确时返回
- **NoMatchingSkill**: 当没有找到匹配的技能时返回

## 2. Implementation (实现)

```python
#!/usr/bin/env python3
"""
策 (ce) - 执行计划制定
根据需求分析结果，制定执行计划，选择合适的技能组合
"""
import sys
import json
import os

# --- Skill Registry (技能注册表) ---
# 映射意图类型到可用技能
INTENT_TO_SKILLS = {
    "search": ["sou"],
    "read": ["du"],
    "write": ["xie"],
    "execute": ["xing"],
    "analyze": ["bi", "lian"],
    "create": ["xie", "hua"],
    "modify": ["gai"],
    "delete": ["jian"]
}

# 实体类型到技能的映射
ENTITY_TO_SKILLS = {
    "file": ["du", "xie", "cun"],
    "url": ["sou", "du"],
    "text": ["du", "xie"],
    "command": ["xing"]
}

# 组合技能（成语）- 常用工作流
COMBO_SKILLS = {
    "搜而读": {"skills": ["sou", "du"], "description": "搜索后读取内容"},
    "搜而写": {"skills": ["sou", "xie"], "description": "搜索后写作"},
    "读而写": {"skills": ["du", "xie"], "description": "读取后写作"},
    "读而比": {"skills": ["du", "bi"], "description": "读取后比较分析"},
    "写而存": {"skills": ["xie", "cun"], "description": "写作后保存"},
    "搜读写存": {"skills": ["sou", "du", "xie", "cun"], "description": "搜索→读取→写作→保存"}
}

# --- Core Logic ---
def match_skills(intent, entities, constraints):
    """匹配适合的技能"""
    plan = []
    used_skills = set()
    
    # 1. 根据意图选择主技能
    intent_type = intent.get("type", "execute")
    if intent_type in INTENT_TO_SKILLS:
        for skill in INTENT_TO_SKILLS[intent_type]:
            if skill not in used_skills:
                plan.append({
                    "skill": skill,
                    "reason": f"匹配意图类型: {intent_type}",
                    "priority": 1
                })
                used_skills.add(skill)
    
    # 2. 根据实体选择辅助技能
    for entity in entities:
        entity_type = entity.get("type", "")
        if entity_type in ENTITY_TO_SKILLS:
            for skill in ENTITY_TO_SKILLS[entity_type]:
                if skill not in used_skills:
                    plan.append({
                        "skill": skill,
                        "reason": f"处理实体: {entity.get('value', '')}",
                        "priority": 2
                    })
                    used_skills.add(skill)
    
    # 3. 根据约束添加技能
    if constraints.get("format") in ["json", "yaml"]:
        if "pei" not in used_skills:
            plan.append({
                "skill": "pei",
                "reason": "格式化输出",
                "priority": 3
            })
    
    # 按优先级排序
    plan.sort(key=lambda x: x["priority"])
    
    return plan

def check_skill_exists(skill_name):
    """检查技能是否存在"""
    skill_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        skill_name
    )
    return os.path.isdir(skill_dir)

def generate_plan(intent, entities, constraints):
    """生成执行计划"""
    # 匹配技能
    skill_matches = match_skills(intent, entities, constraints)
    
    # 检查哪些技能存在
    available_skills = []
    unavailable_skills = []
    
    for match in skill_matches:
        skill = match["skill"]
        if check_skill_exists(skill):
            available_skills.append(match)
        else:
            unavailable_skills.append(skill)
    
    # 构建步骤
    plan = []
    for i, match in enumerate(available_skills, 1):
        plan.append({
            "step": i,
            "skill": match["skill"],
            "input": {},  # 将在执行时填充
            "reason": match["reason"]
        })
    
    # 生成fallback说明
    fallback = ""
    if unavailable_skills:
        fallback = f"以下技能缺失，将跳过: {', '.join(unavailable_skills)}"
    
    return {
        "plan": plan,
        "estimated_steps": len(plan),
        "fallback": fallback
    }

def execute(params):
    # 验证输入
    if not isinstance(params, dict):
        return {"status": "error", "message": "InvalidInput: expected dict"}
    
    intent = params.get("intent", {})
    entities = params.get("entities", [])
    constraints = params.get("constraints", {})
    
    if not intent:
        return {"status": "error", "message": "InvalidInput: intent is required"}
    
    result = generate_plan(intent, entities, constraints)
    return {"status": "success", "data": result}

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
python main.py '{"intent": {"type": "search", "confidence": 0.9, "keywords": ["搜索"]}, "entities": [], "constraints": {}}'
# Expect: {"status": "success", "data": {"plan": [{"step": 1, "skill": "sou", ...}], ...}}
```

### With Entities
```bash
python main.py '{"intent": {"type": "read", "confidence": 0.9, "keywords": []}, "entities": [{"name": "file", "value": "test.py", "type": "file"}], "constraints": {}}'
# Expect: plan includes du skill
```

### Edge Case - No Matching Skills
```bash
python main.py '{"intent": {"type": "unknown", "confidence": 0.5, "keywords": []}, "entities": [], "constraints": {}}'
# Expect: empty plan with fallback message
```
