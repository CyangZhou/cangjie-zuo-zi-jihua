#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自我学习系统 - 仓颉造字计划
记录执行历史，学习成功模式，自动优化
"""

import os
import json
from datetime import datetime

MEMORY_FILE = "skills/dictionary/memory.json"


def load_memory():
    """加载记忆"""
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {"success_patterns": [], "failed_patterns": [], "skills": {}}


def save_memory(memory):
    """保存记忆"""
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)


def learn_success(requirement, intent, plan, result):
    """学习成功模式"""
    memory = load_memory()

    # 记录成功模式
    pattern = {
        "requirement": requirement[:50],
        "intent": intent.get("type", "unknown"),
        "skills": [s.get("skill") for s in plan],
        "timestamp": datetime.now().isoformat(),
    }

    memory["success_patterns"].append(pattern)

    # 保持最近20条
    memory["success_patterns"] = memory["success_patterns"][-20:]

    # 更新技能使用统计
    for s in plan:
        skill_name = s.get("skill", "")
        if skill_name:
            if skill_name not in memory["skills"]:
                memory["skills"][skill_name] = {"success": 0, "failed": 0}
            memory["skills"][skill_name]["success"] += 1

    save_memory(memory)


def learn_failure(requirement, intent, plan, error):
    """学习失败模式"""
    memory = load_memory()

    pattern = {
        "requirement": requirement[:50],
        "intent": intent.get("type", "unknown"),
        "skills": [s.get("skill") for s in plan],
        "error": str(error)[:100],
        "timestamp": datetime.now().isoformat(),
    }

    memory["failed_patterns"].append(pattern)
    memory["failed_patterns"] = memory["failed_patterns"][-20:]

    # 更新失败统计
    for s in plan:
        skill_name = s.get("skill", "")
        if skill_name:
            if skill_name not in memory["skills"]:
                memory["skills"][skill_name] = {"success": 0, "failed": 0}
            memory["skills"][skill_name]["failed"] += 1

    save_memory(memory)


def get_suggested_skills(requirement):
    """根据历史推荐技能"""
    memory = load_memory()
    req_type = None

    # 简单意图检测
    if "搜" in requirement or "索" in requirement:
        req_type = "search"
    elif "写" in requirement or "生成" in requirement:
        req_type = "write"
    elif "读" in requirement or "看" in requirement:
        req_type = "read"

    if not req_type:
        return None

    # 查找相似成功模式
    for pattern in reversed(memory.get("success_patterns", [])):
        if pattern.get("intent") == req_type:
            return pattern.get("skills", [])

    return None


def get_skill_stats():
    """获取技能统计"""
    memory = load_memory()
    return memory.get("skills", {})


# 测试
if __name__ == "__main__":
    print("=== 自我学习系统 ===")
    memory = load_memory()
    print(f"成功模式: {len(memory.get('success_patterns', []))}条")
    print(f"失败模式: {len(memory.get('failed_patterns', []))}条")
    print(f"技能统计: {get_skill_stats()}")
