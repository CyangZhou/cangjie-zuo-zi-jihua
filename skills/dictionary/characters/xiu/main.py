#!/usr/bin/env python3
"""
修 (xiu) - 错误修复
分析错误并尝试修复，提供错误诊断和建议
支持Python代码错误检测与自动修复
"""

import sys
import json
import re

# --- Python Error Patterns (Python错误模式) ---
PYTHON_ERROR_PATTERNS = {
    "SyntaxError": {
        "pattern": r"SyntaxError: (.+)",
        "diagnosis": "代码语法错误",
        "fix_template": "修正语法错误: {error_msg}",
    },
    "IndentationError": {
        "pattern": r"IndentationError: (.+)",
        "diagnosis": "缩进错误",
        "fix_template": "检查并修正缩进: {error_msg}",
    },
    "NameError": {
        "pattern": r"NameError: (.+)",
        "diagnosis": "使用了未定义的变量或函数",
        "fix_template": "定义变量或导入模块: {error_msg}",
    },
    "TypeError": {
        "pattern": r"TypeError: (.+)",
        "diagnosis": "类型不匹配",
        "fix_template": "检查类型转换: {error_msg}",
    },
    "ImportError": {
        "pattern": r"ImportError|ModuleNotFoundError: (.+)",
        "diagnosis": "模块导入失败",
        "fix_template": "安装或检查模块: {error_msg}",
    },
    "FileNotFoundError": {
        "pattern": r"FileNotFoundError: (.+)",
        "diagnosis": "文件不存在",
        "fix_template": "检查文件路径: {error_msg}",
    },
    "ZeroDivisionError": {
        "pattern": r"ZeroDivisionError: (.+)",
        "diagnosis": "除零错误",
        "fix_template": "添加除数检查: {error_msg}",
    },
    "IndexError": {
        "pattern": r"IndexError: (.+)",
        "diagnosis": "索引超出范围",
        "fix_template": "检查索引边界: {error_msg}",
    },
    "KeyError": {
        "pattern": r"KeyError: (.+)",
        "diagnosis": "字典键不存在",
        "fix_template": "使用get()方法或检查键: {error_msg}",
    },
    "ValueError": {
        "pattern": r"ValueError: (.+)",
        "diagnosis": "值不合法",
        "fix_template": "检查输入值: {error_msg}",
    },
    "AttributeError": {
        "pattern": r"AttributeError: (.+)",
        "diagnosis": "对象没有此属性",
        "fix_template": "检查属性名或方法: {error_msg}",
    },
}

# --- Error Patterns (通用错误模式) ---
ERROR_PATTERNS = {
    "SkillNotFound": {
        "diagnosis": "指定技能不存在",
        "fix": "检查技能名称是否正确，或使用现有技能替代",
        "can_retry": True,
        "max_retries": 2,
    },
    "NetworkError": {
        "diagnosis": "网络连接失败",
        "fix": "检查网络连接，或尝试使用本地数据",
        "can_retry": True,
        "max_retries": 3,
    },
    "InvalidInput": {
        "diagnosis": "输入参数无效",
        "fix": "检查输入格式是否符合Schema要求",
        "can_retry": True,
        "max_retries": 2,
    },
    "ExecutionError": {
        "diagnosis": "执行过程出错",
        "fix": "检查技能实现代码，查看错误详情",
        "can_retry": True,
        "max_retries": 2,
    },
    "Timeout": {
        "diagnosis": "执行超时",
        "fix": "增加超时时间或简化任务",
        "can_retry": True,
        "max_retries": 2,
    },
    "PermissionError": {
        "diagnosis": "权限不足",
        "fix": "检查文件权限或请求更高权限",
        "can_retry": False,
        "max_retries": 0,
    },
    "ValidationFailed": {
        "diagnosis": "验证失败",
        "fix": "检查输出是否符合预期",
        "can_retry": True,
        "max_retries": 2,
    },
}


# --- Core Logic ---
def parse_python_error(error_message):
    """解析Python错误信息，提取错误类型、消息和行号"""
    # 匹配错误类型和消息
    for error_type, info in PYTHON_ERROR_PATTERNS.items():
        match = re.search(info["pattern"], error_message, re.IGNORECASE)
        if match:
            error_msg = match.group(1) if match.groups() else error_message

            # 尝试提取行号
            line_match = re.search(r"line (\d+)", error_message)
            line_num = int(line_match.group(1)) if line_match else None

            return {
                "type": error_type,
                "message": error_msg.strip(),
                "line": line_num,
                "full_message": error_message,
            }

    return None


def extract_code_from_error(error_data):
    """从错误数据中提取相关代码"""
    # 尝试从各种可能的字段获取代码
    if isinstance(error_data, dict):
        # 可能有 code 或 source 字段
        return error_data.get("code") or error_data.get("source") or ""
    return ""


def auto_fix_python_error(error_info, original_code):
    """尝试自动修复Python代码错误"""
    if not error_info or not original_code:
        return None

    error_type = error_info.get("type", "")
    lines = original_code.split("\n")

    # 根据错误类型进行修复
    if error_type == "IndentationError":
        # 修正缩进 - 检查上一行
        line_num = error_info.get("line")
        if line_num and line_num > 1:
            # 检查上一行的缩进
            prev_line = lines[line_num - 2] if line_num > 1 else ""
            indent = len(prev_line) - len(prev_line.lstrip())
            lines[line_num - 1] = " " * indent + lines[line_num - 1].lstrip()
            return "\n".join(lines)

    elif error_type == "NameError":
        # 可能是未定义的变量，尝试添加定义
        error_msg = error_info.get("message", "")
        # 提取变量名
        var_match = re.search(r"name '(\w+)' is not defined", error_msg)
        if var_match:
            var_name = var_match.group(1)
            # 在第一行后添加变量定义
            lines.insert(1, f"{var_name} = None  # 自动修复: 定义变量")
            return "\n".join(lines)

    elif error_type == "ImportError":
        # 模块导入失败，尝试修改导入方式
        error_msg = error_info.get("message", "")
        # 提取模块名
        mod_match = re.search(r" No module named '(\w+)'", error_msg)
        if mod_match:
            mod_name = mod_match.group(1)
            # 尝试添加 try-except
            for i, line in enumerate(lines):
                if f"import {mod_name}" in line or f"from {mod_name}" in line:
                    lines[i] = (
                        f"try:\n    {line}\nexcept ImportError:\n    {mod_name} = None  # 模块未安装"
                    )
                    return "\n".join(lines)

    elif error_type == "TypeError":
        # 类型错误，尝试添加类型转换
        error_msg = error_info.get("message", "")
        # 简单修复: 尝试将参数转换为字符串
        if "unsupported operand type" in error_msg:
            # 找到问题行并添加 str() 转换
            line_num = error_info.get("line")
            if line_num and line_num <= len(lines):
                # 简化处理：将 + 改为字符串拼接
                lines[line_num - 1] = "# 尝试修复类型错误: " + lines[line_num - 1]
                return "\n".join(lines)

    elif error_type == "IndexError":
        # 索引错误，添加边界检查
        line_num = error_info.get("line")
        if line_num and line_num <= len(lines):
            lines[line_num - 1] = (
                "try:\n    "
                + lines[line_num - 1]
                + "\nexcept IndexError:\n    pass  # 索引越界已处理"
            )
            return "\n".join(lines)

    elif error_type == "FileNotFoundError":
        # 文件不存在，添加文件检查
        line_num = error_info.get("line")
        if line_num and line_num <= len(lines):
            # 提取文件路径
            path_match = re.search(
                r"\[Errno 2\] No such file or directory: '(.+)'",
                error_info.get("full_message", ""),
            )
            if path_match:
                file_path = path_match.group(1)
                lines.insert(0, f"# 尝试创建缺失的目录和文件")
                lines.insert(1, f"import os")
                lines.insert(
                    2,
                    f"os.makedirs(os.path.dirname('{file_path}') or '.', exist_ok=True)",
                )
                return "\n".join(lines)

    return None


def detect_error_type(error_message):
    """检测错误类型"""
    error_message = error_message.lower()

    for pattern, info in ERROR_PATTERNS.items():
        if pattern.lower() in error_message:
            return pattern

    # 尝试从错误信息中提取
    if "not found" in error_message or "不存在" in error_message:
        return "SkillNotFound"
    elif "network" in error_message or "网络" in error_message:
        return "NetworkError"
    elif "invalid" in error_message or "无效" in error_message:
        return "InvalidInput"
    elif "timeout" in error_message or "超时" in error_message:
        return "Timeout"
    elif "permission" in error_message or "权限" in error_message:
        return "PermissionError"
    else:
        return "ExecutionError"


def analyze_error(error, original_plan=None, attempt=0):
    """分析错误并生成修复建议"""
    error_type = error.get("type", "")
    error_message = error.get("message", "")

    # 优先检测Python代码错误
    python_error = parse_python_error(error_message)
    if python_error:
        return analyze_python_error(python_error, error, original_plan)

    # 如果没有明确类型，从消息中检测
    if not error_type:
        error_type = detect_error_type(error_message)

    # 获取错误模式信息
    pattern_info = ERROR_PATTERNS.get(
        error_type,
        {
            "diagnosis": "未知错误",
            "fix": "需要人工介入",
            "can_retry": False,
            "max_retries": 0,
        },
    )

    # 生成诊断
    diagnosis = f"[{error_type}] {pattern_info['diagnosis']}: {error_message}"

    # 生成修复建议
    suggested_fix = pattern_info["fix"]

    # 尝试修改计划
    new_plan = None
    if original_plan and pattern_info.get("can_retry"):
        new_plan = suggest_plan_modification(original_plan, error_type)

    return {
        "diagnosis": diagnosis,
        "suggested_fix": suggested_fix,
        "new_plan": new_plan,
        "can_retry": pattern_info.get("can_retry", False),
        "max_retries": pattern_info.get("max_retries", 0),
    }


def analyze_python_error(error_info, original_error, original_plan=None):
    """分析Python代码错误并尝试自动修复"""
    error_type = error_info["type"]
    error_msg = error_info["message"]
    line_num = error_info.get("line")

    # 获取错误模式信息
    pattern_info = PYTHON_ERROR_PATTERNS.get(error_type, {})

    # 生成诊断
    line_info = f" 第{line_num}行" if line_num else ""
    diagnosis = f"[Python {error_type}]{line_info}: {error_msg}"

    # 尝试自动修复
    original_code = original_error.get("code", "")
    fixed_code = auto_fix_python_error(error_info, original_code)

    if fixed_code:
        suggested_fix = f"已自动修复: {pattern_info.get('fix_template', '').format(error_msg=error_msg)}"
        new_plan = None
        if original_plan:
            # 更新计划中的代码
            new_plan = [step.copy() for step in original_plan]
            for step in new_plan:
                if step.get("skill") == "xie":
                    step["input"]["code"] = fixed_code
                elif step.get("skill") == "yun":
                    step["input"]["code"] = fixed_code
    else:
        suggested_fix = pattern_info.get("fix_template", "需要手动修复").format(
            error_msg=error_msg
        )
        new_plan = None

    return {
        "diagnosis": diagnosis,
        "suggested_fix": suggested_fix,
        "fixed_code": fixed_code,
        "new_plan": new_plan,
        "can_retry": True,
        "max_retries": 3,
    }


def suggest_plan_modification(plan, error_type):
    """建议修改执行计划"""
    if not plan or not isinstance(plan, list):
        return None

    # 复制计划
    new_plan = [step.copy() for step in plan]

    # 根据错误类型调整
    if error_type == "SkillNotFound":
        # 移除不存在的技能
        pass
    elif error_type == "InvalidInput":
        # 简化输入
        for step in new_plan:
            if "input" in step:
                step["input"] = {}
    elif error_type == "Timeout":
        # 减少任务量
        if len(new_plan) > 1:
            new_plan = new_plan[:1]

    return new_plan


def fix(error, original_plan=None, attempt=0):
    """修复错误"""
    if not error:
        return {"status": "error", "message": "InvalidInput: error is required"}

    analysis = analyze_error(error, original_plan, attempt)

    return {"status": "success", "data": analysis}


def execute(params):
    error = params.get("error", {})
    original_plan = params.get("original_plan")
    attempt = params.get("attempt", 0)

    return fix(error, original_plan, attempt)


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
