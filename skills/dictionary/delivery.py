#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交付系统 - 仓颉造字计划
让系统真正"好用"：
1. 结果可视化展示
2. 错误解释为中文
3. 使用指引生成
4. 交互式引导
"""

import json
import os
from datetime import datetime

# --- 错误翻译字典 ---
ERROR_TRANSLATIONS = {
    # 网络错误
    "NetworkError": "网络问题",
    "timeout": "网络超时",
    "Connection refused": "连接被拒绝",
    "404": "找不到内容",
    "403": "没有访问权限",
    "500": "服务器出错",
    # 文件错误
    "FileNotFoundError": "文件不存在",
    "Permission denied": "没有权限",
    "Is a directory": "这是文件夹，不是文件",
    "Not a directory": "这不是文件夹",
    # 代码执行错误
    "SyntaxError": "代码语法有误",
    "IndentationError": "代码缩进不对",
    "NameError": "使用了未定义的名称",
    "TypeError": "数据类型不匹配",
    "ValueError": "值不符合要求",
    "ImportError": "缺少需要的模块",
    "ModuleNotFoundError": "缺少某个工具包",
    "IndexError": "数组索引越界",
    "KeyError": "字典找不到这个键",
    "AttributeError": "对象没有这个属性",
    "ZeroDivisionError": "除数为零",
    # 权限/认证
    "Unauthorized": "未登录或登录已过期",
    "Forbidden": "没有权限执行此操作",
    "authentication": "需要登录",
    # 通用
    "error": "出了点问题",
    "failed": "执行失败",
    "exception": "遇到异常",
}

# --- 技能说明字典 ---
SKILL_GUIDES = {
    "sou": "搜索功能 - 帮你找到网上的信息",
    "du": "读取功能 - 读取网页或本地文件",
    "xie": "写作功能 - 生成内容或代码",
    "cun": "保存功能 - 保存结果到文件",
    "bi": "比较功能 - 对比分析两个内容",
    "yun": "运行功能 - 执行生成的代码",
    "hua": "画图功能 - 生成简单图形",
    "fa": "发送功能 - 发送内容",
    "ji": "记录功能 - 记录和记忆信息",
    "kong": "控制功能 - 控制操作",
    "dong": "理解 - 分析你的需求",
    "ce": "策划 - 制定执行计划",
    "xing": "执行 - 真正干活",
    "yan": "验证 - 检查结果对不对",
    "xiu": "修复 - 自动修复问题",
}


def explain_error(error_msg, skill_name=None):
    """
    将技术错误转化为通俗中文

    Args:
        error_msg: 原始错误信息
        skill_name: 出错的技能名称

    Returns:
        dict: 解释结果
    """
    if not error_msg:
        return {
            "status": "success",
            "data": {
                "chinese": "出了点问题，但不清楚具体是什么",
                "technical": error_msg,
                "suggestion": "可以尝试重新描述一下你的需求",
            },
        }

    error_lower = str(error_msg).lower()
    chinese_errors = []

    # 匹配错误翻译
    for eng, chi in ERROR_TRANSLATIONS.items():
        if eng.lower() in error_lower:
            chinese_errors.append(chi)

    if chinese_errors:
        chinese_msg = "，".join(chinese_errors)
    else:
        chinese_msg = "执行过程中遇到了问题"

    # 生成建议
    suggestions = []
    if "网络" in chinese_msg or "超时" in chinese_msg:
        suggestions.append("请检查网络连接是否正常")
        suggestions.append("可以稍后再试")
    elif "不存在" in chinese_msg or "找不到" in chinese_msg:
        suggestions.append("请确认文件路径或链接是否正确")
    elif "权限" in chinese_msg:
        suggestions.append("可能需要管理员权限或登录")
    elif "缺少" in chinese_msg or "模块" in chinese_msg:
        suggestions.append("系统正在自动处理")
    else:
        suggestions.append("可以尝试换一种方式描述需求")
        suggestions.append("或者把问题描述得更详细一些")

    # 技能相关建议
    if skill_name and skill_name in SKILL_GUIDES:
        suggestions.append(f"使用 {SKILL_GUIDES[skill_name]}")

    return {
        "status": "success",
        "data": {
            "chinese": chinese_msg,
            "technical": error_msg,
            "suggestion": "；".join(suggestions),
            "skill_tip": SKILL_GUIDES.get(skill_name, ""),
        },
    }


def format_result(result, requirement):
    """
    将执行结果格式化为用户友好的展示

    Args:
        result: 执行结果
        requirement: 用户原始需求

    Returns:
        dict: 格式化后的结果
    """
    if not result:
        return {
            "status": "success",
            "data": {
                "display": "没有返回结果",
                "type": "empty",
            },
        }

    result_type = "text"
    display = ""

    # 提取关键数据
    data = result.get("data", result) if isinstance(result, dict) else result

    # 根据数据类型选择展示方式
    if isinstance(data, dict):
        # 检查是否有特定类型的输出
        if "result" in data:
            content = data["result"]
            if isinstance(content, str):
                # 尝试识别内容类型
                if content.startswith("[图形]"):
                    result_type = "image"
                    display = f"[图片] {content[5:]}"
                elif content.startswith("[代码]"):
                    result_type = "code"
                    display = f"[代码] {content[5:]}"
                elif "http" in content:
                    result_type = "link"
                    display = f"[链接] {content}"
                else:
                    result_type = "text"
                    display = content[:500]  # 截断太长内容
            else:
                display = str(content)[:500]
        elif "content" in data:
            content = data["content"]
            if isinstance(content, str):
                display = content[:500]
            else:
                display = str(content)[:500]
        else:
            # 通用dict展示
            display = json.dumps(data, ensure_ascii=False, indent=2)[:500]
    elif isinstance(data, list):
        display = "\n".join(str(item)[:100] for item in data[:5])
        if len(data) > 5:
            display += f"\n...还有 {len(data) - 5} 条"
    elif isinstance(data, str):
        display = data[:500]
    else:
        display = str(data)[:500]

    return {
        "status": "success",
        "data": {
            "display": display,
            "type": result_type,
            "raw": result,
            "timestamp": datetime.now().isoformat(),
        },
    }


def generate_guide(requirement, result, status):
    """
    生成使用指引和建议

    Args:
        requirement: 用户需求
        result: 执行结果
        status: 执行状态 (success/error)

    Returns:
        dict: 指引建议
    """
    guides = []

    if status == "success":
        # 成功的指引
        guides.append(
            {
                "title": "[OK] 完成了！",
                "content": "你的需求已经处理完成",
                "actions": [
                    {"label": "查看结果", "type": "show"},
                    {"label": "保存结果", "action": "cun"},
                    {"label": "继续下一个", "type": "continue"},
                ],
            }
        )

        # 根据需求类型给出建议
        if "搜索" in requirement or "找" in requirement:
            guides.append(
                {
                    "title": "[INFO] 搜索结果使用提示",
                    "content": "可以让我读取详细内容，或者保存到本地",
                    "actions": [
                        {"label": "读取", "action": "du"},
                        {"label": "保存", "action": "cun"},
                    ],
                }
            )
        elif "写" in requirement or "生成" in requirement:
            guides.append(
                {
                    "title": "[INFO] 生成内容提示",
                    "content": "可以运行生成的代码，或修改后重新生成",
                    "actions": [
                        {"label": "运行代码", "action": "yun"},
                        {"label": "修改需求", "type": "modify"},
                    ],
                }
            )
    else:
        # 失败的指引
        guides.append(
            {
                "title": "[WARN] 遇到了问题",
                "content": "让我帮你分析和解决",
                "actions": [
                    {"label": "重试", "type": "retry"},
                    {"label": "换个方式", "type": "modify"},
                    {"label": "获取帮助", "type": "help"},
                ],
            }
        )

        # 分析可能的原因
        if "网络" in str(result) or "超时" in str(result):
            guides.append(
                {
                    "title": "[INFO] 可能原因",
                    "content": "网络连接可能不稳定",
                    "actions": [
                        {"label": "重试", "type": "retry"},
                        {"label": "换个方式", "type": "modify"},
                        {"label": "获取帮助", "type": "help"},
                    ],
                }
            )

        # 分析可能的原因
        if "网络" in str(result) or "超时" in str(result):
            guides.append(
                {
                    "title": "💡 可能原因",
                    "content": "网络连接可能不稳定",
                    "actions": [
                        {"label": "重试", "type": "retry"},
                    ],
                }
            )

    # 通用指引
    guides.append(
        {
            "title": "[MORE] 更多操作",
            "content": "你可以：",
            "actions": [
                {"label": "搜索", "action": "sou"},
                {"label": "读取", "action": "du"},
                {"label": "写作", "action": "xie"},
                {"label": "保存", "action": "cun"},
                {"label": "比较", "action": "bi"},
            ],
        }
    )

    return {
        "status": "success",
        "data": {
            "guides": guides,
            "quick_actions": [a for g in guides for a in g.get("actions", [])],
        },
    }


def interactive_prompt(requirement, step, context=None):
    """
    生成交互式引导提示

    Args:
        requirement: 当前需求
        step: 当前步骤
        context: 上下文信息

    Returns:
        dict: 引导提示
    """
    prompts = {
        "start": {
            "message": f'我理解你的需求是："{requirement}"',
            "question": "这样理解对吗？还是需要修改？",
            "options": [
                {"label": "对的，继续", "action": "continue"},
                {"label": "修改需求", "action": "modify"},
                {"label": "取消", "action": "cancel"},
            ],
        },
        "planning": {
            "message": "我计划这样执行：",
            "question": "要调整执行计划吗？",
            "options": [
                {"label": "按计划执行", "action": "continue"},
                {"label": "修改计划", "action": "modify_plan"},
                {"label": "取消", "action": "cancel"},
            ],
        },
        "result": {
            "message": "处理完成！",
            "question": "需要做什么？",
            "options": [
                {"label": "查看详情", "action": "show"},
                {"label": "保存结果", "action": "cun"},
                {"label": "继续下一个", "action": "continue"},
            ],
        },
        "error": {
            "message": "出了点问题",
            "question": "怎么处理？",
            "options": [
                {"label": "重试", "action": "retry"},
                {"label": "换个方式", "action": "modify"},
                {"label": "放弃", "action": "cancel"},
            ],
        },
    }

    prompt = prompts.get(step, prompts["start"])

    return {
        "status": "success",
        "data": {
            **prompt,
            "context": context or {},
        },
    }


def deliver(requirement, result, status="success", include_guide=True):
    """
    统一的交付接口 - 整合所有交付能力

    Args:
        requirement: 用户需求
        result: 执行结果
        status: 执行状态
        include_guide: 是否包含指引

    Returns:
        dict: 完整的交付内容
    """
    delivery = {
        "status": "success",
        "requirement": requirement,
        "timestamp": datetime.now().isoformat(),
    }

    # 1. 结果可视化
    format_res = format_result(result, requirement)
    delivery["display"] = format_res["data"]

    # 2. 错误解释（如果有错误）
    if status == "error":
        error_msg = (
            result.get("message", "") if isinstance(result, dict) else str(result)
        )
        skill_name = result.get("skill") if isinstance(result, dict) else None
        error_exp = explain_error(error_msg, skill_name)
        delivery["explanation"] = error_exp["data"]
    else:
        delivery["explanation"] = None

    # 3. 使用指引
    if include_guide:
        guide = generate_guide(requirement, result, status)
        delivery["guide"] = guide["data"]

    return delivery


# --- 测试 ---
if __name__ == "__main__":
    print("=== 交付系统测试 ===")

    # 测试错误翻译
    print("\n1. 错误翻译测试：")
    test_errors = [
        "FileNotFoundError: test.txt",
        "timeout connecting to server",
        "SyntaxError: invalid syntax",
        "ModuleNotFoundError: No module named 'requests'",
    ]
    for err in test_errors:
        result = explain_error(err)
        print(f"  原文: {err}")
        print(f"  翻译: {result['data']['chinese']}")
        print(f"  建议: {result['data']['suggestion']}")
        print()

    # 测试结果格式化
    print("\n2. 结果格式化测试：")
    test_result = {"data": {"result": "搜索到10条结果：Python教程、JavaScript教程..."}}
    formatted = format_result(test_result, "搜索Python教程")
    print(f"  展示: {formatted['data']['display'][:50]}...")
    print(f"  类型: {formatted['data']['type']}")

    # 测试指引生成
    print("\n3. 指引生成测试：")
    guide = generate_guide("搜索Python教程", {}, "success")
    print(f"  指引数量: {len(guide['data']['guides'])}")
    for g in guide["data"]["guides"]:
        print(f"  - {g['title']}: {g['content']}")

    # 测试完整交付
    print("\n4. 完整交付测试：")
    delivery = deliver(
        "搜索Python教程", {"data": {"result": "找到相关内容"}}, "success"
    )
    print(f"  可视化: {delivery['display']['type']}")
    print(f"  指引: {'有' if delivery.get('guide') else '无'}")
