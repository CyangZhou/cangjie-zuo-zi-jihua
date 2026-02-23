---
name: xiu
description: 分析错误并尝试修复，提供错误诊断和建议
tags: [fix, repair, error, debugging, diagnostics]
dependencies: []
五行: 木
---

# 修 (Character: xiu)

## 1. IO Contract (契约)

### Input Schema (JSON)
```json
{
  "error": {
    "type": "string (错误类型)",
    "message": "string (错误信息)",
    "context": "object (错误上下文)"
  },
  "original_plan": "object (原始执行计划)",
  "attempt": "integer (修复尝试次数)"
}
```

### Output Schema (JSON)
```json
{
  "status": "success | error",
  "data": {
    "diagnosis": "string (错误诊断)",
    "suggested_fix": "string (建议修复方案)",
    "new_plan": "object (修改后的执行计划)",
    "can_retry": "boolean (是否可以重试)",
    "max_retries": "integer (最大重试次数)"
  }
}
```

### Failure Modes
- **Unrecoverable**: 当错误无法恢复时返回
- **MaxRetriesExceeded**: 当超过最大重试次数时返回

## 2. Implementation (实现)

```python
#!/usr/bin/env python3
"""
修 (xiu) - 错误修复
分析错误并尝试修复，提供错误诊断和建议
"""
import sys
import json
import re

# --- Error Patterns (错误模式) ---
ERROR_PATTERNS = {
    "SkillNotFound": {
        "diagnosis": "指定技能不存在",
        "fix": "检查技能名称是否正确，或使用现有技能替代",
        "can_retry": True,
        "max_retries": 2
    },
    "NetworkError": {
        "diagnosis": "网络连接失败",
        "fix": "检查网络连接，或尝试使用本地数据",
        "can_retry": True,
        "max_retries": 3
    },
    "InvalidInput": {
        "diagnosis": "输入参数无效",
        "fix": "检查输入格式是否符合Schema要求",
        "can_retry": True,
        "max_retries": 2
    },
    "ExecutionError": {
        "diagnosis": "执行过程出错",
        "fix": "检查技能实现代码，查看错误详情",
        "can_retry": True,
        "max_retries": 2
    },
    "Timeout": {
        "diagnosis": "执行超时",
        "fix": "增加超时时间或简化任务",
        "can_retry": True,
        "max_retries": 2
    },
    "PermissionError": {
        "diagnosis": "权限不足",
        "fix": "检查文件权限或请求更高权限",
        "can_retry": False,
        "max_retries": 0
    }
}

# --- Core Logic ---
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

def analyze_error(error, original_plan, attempt=0):
    """分析错误并生成修复建议"""
    error_type = error.get("type", "")
    error_message = error.get("message", "")
    
    # 如果没有明确类型，从消息中检测
    if not error_type:
        error_type = detect_error_type(error_message)
    
    # 获取错误模式信息
    pattern_info = ERROR_PATTERNS.get(error_type, {
        "diagnosis": "未知错误",
        "fix": "需要人工介入",
        "can_retry": False,
        "max_retries": 0
    })
    
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
        "max_retries": pattern_info.get("max_retries", 0)
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
        # 这里简化处理，实际应该检查技能是否存在
        pass
    elif error_type == "InvalidInput":
        # 简化输入
        for step in new_plan:
            if "input" in step:
                step["input"] = {}  # 清空可能有问题的输入
    elif error_type == "Timeout":
        # 减少任务量
        if len(new_plan) > 1:
            new_plan = new_plan[:1]  # 只执行第一步
    
    return new_plan

def fix(error, original_plan=None, attempt=0):
    """修复错误"""
    if not error:
        return {
            "status": "error",
            "message": "InvalidInput: error is required"
        }
    
    analysis = analyze_error(error, original_plan, attempt)
    
    return {
        "status": "success",
        "data": analysis
    }

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
        print(json.dumps({"status": "error", "message": f"InvalidFormat: {str(e)}"}), file=sys.stderr)
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}), file=sys.stderr)
        sys.exit(1)
```

## 3. Tests & Examples (测试)

### Happy Path
```bash
python main.py '{"error": {"type": "NetworkError", "message": "Connection failed"}}'
# Expect: {"status": "success", "data": {"diagnosis": "...", "suggested_fix": "...", "can_retry": true}}
```

### Unrecoverable Error
```bash
python main.py '{"error": {"type": "PermissionError", "message": "Access denied"}}'
# Expect: {"status": "success", "data": {"can_retry": false, ...}}
```

### Auto-detect Error Type
```bash
python main.py '{"error": {"message": "Skill not found: xxx"}}'
# Expect: auto-detected as SkillNotFound
```
