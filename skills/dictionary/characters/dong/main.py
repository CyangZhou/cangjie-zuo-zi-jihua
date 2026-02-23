#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
懂 (dong) - 中文意图理解
理解中文需求描述，提取意图、实体和约束条件
"""

import sys
import io
import json
import re

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# --- Intent Patterns (意图模式) ---
INTENT_PATTERNS = {
    "search": [
        r"搜索",
        r"查找",
        r"找一下",
        r"帮我找",
        r"查询",
        r"搜",
    ],
    "read": [
        r"读取",
        r"打开",
        r"看",
        r"查看",
        r"显示",
        r"展示",
        r"内容",
        r"文件",
        r"文章",
        r"资料",
    ],
    "write": [
        r"写",
        r"创建",
        r"生成",
        r"制作",
        r"新增",
        r"添加",
        r"编辑",
        r"修改",
        r"更新",
    ],
    "execute": [
        r"运行",
        r"执行",
        r"跑",
        r"启动",
        r"开始",
        r"完成",
        r"实现",
    ],
    "analyze": [r"分析", r"统计", r"计算", r"比较", r"评估", r"检查", r"验证", r"测试"],
    "create": [r"新建", r"开发", r"构建", r"编程", r"写代码"],
    "modify": [r"改", r"修复", r"优化", r"改进", r"调整"],
    "delete": [r"删除", r"移除", r"清除", r"去掉"],
}

# --- Entity Patterns (实体模式) ---
ENTITY_PATTERNS = {
    "file": [r"[^\s]+\.(py|js|ts|md|txt|json|yaml|yml|xml|html|css)", r"文件[^\s]*"],
    "url": [r"https?://[^\s]+", r"网站[^\s]*", r"链接[^\s]*"],
    "command": [r"命令[^\s]*", r"指令[^\s]*", r"终端[^\s]*"],
}


# --- Core Logic ---
def extract_intent(text):
    """提取意图类型"""
    # 扩展意图关键词
    has_search = "搜" in text or "索" in text or "找" in text or "查" in text
    has_read = "读" in text or "看" in text or "显" in text or "示" in text
    has_write = "写" in text or "生成" in text or "创建" in text or "画" in text
    has_analyze = "分析" in text or "比" in text or "较" in text or "对比" in text
    has_send = "发" in text or "送" in text or "邮件" in text
    has_control = "控" in text or "制" in text or "执行" in text
    has_remember = "记" in text or "忆" in text or "存" in text

    if has_search:
        return {"type": "search", "confidence": 0.9, "keywords": [text]}
    if has_read:
        return {"type": "read", "confidence": 0.9, "keywords": [text]}
    if has_write:
        return {"type": "write", "confidence": 0.9, "keywords": [text]}
    if has_analyze:
        return {"type": "analyze", "confidence": 0.9, "keywords": [text]}
    if has_send:
        return {"type": "send", "confidence": 0.9, "keywords": [text]}
    if has_remember:
        return {"type": "remember", "confidence": 0.9, "keywords": [text]}
    if has_control:
        return {"type": "control", "confidence": 0.9, "keywords": [text]}

    return {"type": "execute", "confidence": 0.5, "keywords": [text]}


def extract_entities(text):
    """提取实体"""
    entities = []

    # 提取文件路径
    file_pattern = r"([^\s]+\.(py|js|ts|md|txt|json|yaml|yml|xml|html|css))"
    for match in re.finditer(file_pattern, text):
        entities.append({"name": "file", "value": match.group(1), "type": "file"})

    # 提取URL
    url_pattern = r"(https?://[^\s]+)"
    for match in re.finditer(url_pattern, text):
        entities.append({"name": "url", "value": match.group(1), "type": "url"})

    return entities


def extract_constraints(text):
    """提取约束条件"""
    constraints = {}

    # 格式要求
    format_match = re.search(
        r"(json|yaml|xml|csv|markdown|html|python|javascript)", text, re.IGNORECASE
    )
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
        "delete": "使用'删'技能执行删除",
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
        "action_plan": "",
    }
    result["action_plan"] = generate_action_plan(
        result["intent"]["type"], result["entities"], result["constraints"]
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
        print(
            json.dumps({"status": "error", "message": f"InvalidFormat: {str(e)}"}),
            file=sys.stderr,
        )
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}), file=sys.stderr)
        sys.exit(1)
