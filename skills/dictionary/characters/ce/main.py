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
    "execute": ["sou"],  # 通用执行默认使用搜索
    "analyze": ["bi", "lian"],
    "create": ["xie", "hua"],
    "modify": ["gai"],
    "delete": ["jian"],
}

# 实体类型到技能的映射
ENTITY_TO_SKILLS = {
    "file": ["du", "xie", "cun"],
    "url": ["sou", "du"],
    "text": ["du", "xie"],
    "command": ["xing"],
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
                plan.append(
                    {
                        "skill": skill,
                        "reason": f"匹配意图类型: {intent_type}",
                        "priority": 1,
                    }
                )
                used_skills.add(skill)

    # 2. 根据实体选择辅助技能
    for entity in entities:
        entity_type = entity.get("type", "")
        if entity_type in ENTITY_TO_SKILLS:
            for skill in ENTITY_TO_SKILLS[entity_type]:
                if skill not in used_skills:
                    plan.append(
                        {
                            "skill": skill,
                            "reason": f"处理实体: {entity.get('value', '')}",
                            "priority": 2,
                        }
                    )
                    used_skills.add(skill)

    # 3. 根据约束添加技能
    if constraints.get("format") in ["json", "yaml"]:
        if "pei" not in used_skills:
            plan.append({"skill": "pei", "reason": "格式化输出", "priority": 3})

    # 按优先级排序
    plan.sort(key=lambda x: x["priority"])

    return plan


def check_skill_exists(skill_name):
    """检查技能是否存在"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    skill_dir = os.path.join(base_dir, skill_name)
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
        skill = match["skill"]

        # 根据技能类型自动填充默认输入
        auto_input = {}
        if skill == "sou":
            # 从意图关键词提取搜索词
            keywords = intent.get("keywords", [])
            if keywords:
                auto_input = {"keywords": " ".join(keywords)}
            else:
                auto_input = {"keywords": "test"}  # 默认搜索词
        elif skill == "xie":
            # 传递完整的需求描述给写技能
            requirement = intent.get("keywords", [""])[0]
            if requirement:
                auto_input = {"description": requirement, "text": requirement}
            else:
                auto_input = {"description": "generate content", "text": "content"}
        elif skill in ["du", "cun"]:
            # 从实体中提取值
            if entities:
                for e in entities:
                    if e.get("type") == "file":
                        auto_input = {"path": e.get("value", "")}
                        break

        plan.append(
            {
                "step": i,
                "skill": skill,
                "input": auto_input,
                "reason": match["reason"],
            }
        )

    # 生成fallback说明
    fallback = ""
    if unavailable_skills:
        fallback = f"以下技能缺失，将跳过: {', '.join(unavailable_skills)}"

    return {"plan": plan, "estimated_steps": len(plan), "fallback": fallback}


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
        print(
            json.dumps({"status": "error", "message": f"InvalidFormat: {str(e)}"}),
            file=sys.stderr,
        )
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}), file=sys.stderr)
        sys.exit(1)
