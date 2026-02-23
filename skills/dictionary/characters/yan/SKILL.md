---
name: yan
description: 验证执行结果是否符合预期，输出验证报告
tags: [validation, verification, testing, quality]
dependencies: []
五行: 火
---

# 验 (Character: yan)

## 1. IO Contract (契约)

### Input Schema (JSON)
```json
{
  "result": "object (执行结果)",
  "expectations": {
    "status": "string (预期状态: success|error|any)",
    "has_data": "boolean (是否期望有数据)",
    "data_type": "string (期望的数据类型: array|object|string|number)",
    "required_fields": ["string", ...] (必需字段),
    "custom_check": "function (自定义验证函数)"
  }
}
```

### Output Schema (JSON)
```json
{
  "status": "success | error",
  "data": {
    "passed": "boolean",
    "checks": [
      {
        "name": "string (检查项名称)",
        "passed": "boolean",
        "message": "string (检查结果描述)"
      }
    ],
    "summary": "string (验证总结)"
  }
}
```

### Failure Modes
- **InvalidInput**: 当输入格式不正确时返回
- **ValidationError**: 当验证失败时返回（但仍返回检查结果）

## 2. Implementation (实现)

```python
#!/usr/bin/env python3
"""
验 (yan) - 结果验证
验证执行结果是否符合预期，输出验证报告
"""
import sys
import json

# --- Core Logic ---
def check_status(result, expected_status):
    """检查状态"""
    result_status = result.get("status", "unknown")
    passed = expected_status == "any" or result_status == expected_status
    return {
        "name": "status_check",
        "passed": passed,
        "message": f"Expected: {expected_status}, Got: {result_status}"
    }

def check_has_data(result, expected):
    """检查是否有数据"""
    data = result.get("data")
    has_data = data is not None and data != {}
    
    if expected and not has_data:
        return {
            "name": "has_data_check",
            "passed": False,
            "message": "Expected data but got empty/null"
        }
    
    if not expected and has_data:
        return {
            "name": "has_data_check",
            "passed": False,
            "message": "Expected no data but got data"
        }
    
    return {
        "name": "has_data_check",
        "passed": True,
        "message": "Data check passed" if has_data else "No data as expected"
    }

def check_data_type(result, expected_type):
    """检查数据类型"""
    data = result.get("data")
    
    if data is None:
        return {
            "name": "data_type_check",
            "passed": False,
            "message": "No data to check type"
        }
    
    actual_type = type(data).__name__
    type_mapping = {
        "array": list,
        "object": dict,
        "string": str,
        "number": (int, float),
        "bool": bool
    }
    
    expected_class = type_mapping.get(expected_type)
    if expected_class is None:
        return {
            "name": "data_type_check",
            "passed": False,
            "message": f"Unknown type: {expected_type}"
        }
    
    passed = isinstance(data, expected_class)
    return {
        "name": "data_type_check",
        "passed": passed,
        "message": f"Expected: {expected_type}, Got: {actual_type}"
    }

def check_required_fields(result, required_fields):
    """检查必需字段"""
    data = result.get("data", {})
    
    if not isinstance(data, dict):
        return {
            "name": "required_fields_check",
            "passed": False,
            "message": "Data is not an object, cannot check fields"
        }
    
    missing = [f for f in required_fields if f not in data]
    
    if missing:
        return {
            "name": "required_fields_check",
            "passed": False,
            "message": f"Missing required fields: {', '.join(missing)}"
        }
    
    return {
        "name": "required_fields_check",
        "passed": True,
        "message": f"All required fields present: {', '.join(required_fields)}"
    }

def validate(result, expectations):
    """执行验证"""
    checks = []
    
    # 检查状态
    if "status" in expectations:
        checks.append(check_status(result, expectations["status"]))
    
    # 检查是否有数据
    if "has_data" in expectations:
        checks.append(check_has_data(result, expectations["has_data"]))
    
    # 检查数据类型
    if "data_type" in expectations:
        checks.append(check_data_type(result, expectations["data_type"]))
    
    # 检查必需字段
    if "required_fields" in expectations:
        checks.append(check_required_fields(result, expectations["required_fields"]))
    
    # 汇总结果
    passed = all(c["passed"] for c in checks)
    
    if passed:
        summary = "All checks passed"
    else:
        failed = [c["name"] for c in checks if not c["passed"]]
        summary = f"Failed checks: {', '.join(failed)}"
    
    return {
        "status": "success",  # 总是返回success，验证结果在data中
        "data": {
            "passed": passed,
            "checks": checks,
            "summary": summary
        }
    }

def execute(params):
    result = params.get("result", {})
    expectations = params.get("expectations", {})
    
    if not result:
        return {"status": "error", "message": "InvalidInput: result is required"}
    
    return validate(result, expectations)

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
python main.py '{"result": {"status": "success", "data": {"results": []}}, "expectations": {"status": "success"}}'
# Expect: {"status": "success", "data": {"passed": true, ...}}
```

### Failed Check
```bash
python main.py '{"result": {"status": "error", "data": {}}, "expectations": {"status": "success"}}'
# Expect: {"status": "success", "data": {"passed": false, ...}}
```

### Required Fields
```bash
python main.py '{"result": {"status": "success", "data": {"count": 5}}, "expectations": {"required_fields": ["count", "results"]}}'
# Expect: {"status": "success", "data": {"passed": false, "checks": [...]}}
```
