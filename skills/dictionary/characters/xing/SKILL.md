---
name: xing
description: 技能执行引擎，按计划顺序调用各个技能执行任务
tags: [execution, runner, workflow, automation]
dependencies: []
五行: 金
---

# 行 (Character: xing)

## 1. IO Contract (契约)

### Input Schema (JSON)
```json
{
  "plan": [
    {
      "step": "integer (步骤序号)",
      "skill": "string (技能名)",
      "input": "object (输入参数)"
    }
  ],
  "context": "object (可选，全局上下文)"
}
```

### Output Schema (JSON)
```json
{
  "status": "success | error | partial",
  "data": {
    "results": [
      {
        "step": "integer",
        "skill": "string",
        "status": "success | error",
        "output": "object",
        "error": "string (如有)"
      }
    ],
    "final_output": "object (最后一步的输出)",
    "executed_steps": "integer",
    "failed_steps": "integer"
  }
}
```

### Failure Modes
- **SkillNotFound**: 当指定的技能不存在时返回
- **ExecutionError**: 当技能执行失败时返回
- **InvalidPlan**: 当执行计划格式不正确时返回

## 2. Implementation (实现)

```python
#!/usr/bin/env python3
"""
行 (xing) - 技能执行引擎
按计划顺序调用各个技能执行任务
"""
import sys
import json
import os
import subprocess
import traceback

# --- Core Logic ---
def get_skill_path(skill_name):
    """获取技能路径"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    skill_dir = os.path.join(base_dir, skill_name)
    main_file = os.path.join(skill_dir, "main.py")
    
    if os.path.isfile(main_file):
        return main_file
    return None

def execute_skill(skill_name, input_params):
    """执行单个技能"""
    skill_path = get_skill_path(skill_name)
    
    if not skill_path:
        return {
            "status": "error",
            "output": None,
            "error": f"Skill not found: {skill_name}"
        }
    
    try:
        # 准备输入
        input_json = json.dumps(input_params, ensure_ascii=False)
        
        # 执行技能
        result = subprocess.run(
            [sys.executable, skill_path],
            input=input_json,
            capture_output=True,
            text=True,
            timeout=60,
            encoding='utf-8',
            errors='replace'
        )
        
        if result.returncode != 0:
            return {
                "status": "error",
                "output": None,
                "error": result.stderr or "Execution failed"
            }
        
        # 解析输出
        try:
            output = json.loads(result.stdout)
            return {
                "status": "success",
                "output": output,
                "error": None
            }
        except json.JSONDecodeError as e:
            return {
                "status": "error",
                "output": None,
                "error": f"Invalid JSON output: {str(e)}"
            }
    
    except subprocess.TimeoutExpired:
        return {
            "status": "error",
            "output": None,
            "error": "Execution timeout"
        }
    except Exception as e:
        return {
            "status": "error",
            "output": None,
            "error": traceback.format_exc()
        }

def build_context(previous_results, global_context):
    """构建传递给下一步的上下文"""
    context = global_context.copy() if global_context else {}
    
    # 将之前的结果添加到上下文
    for result in previous_results:
        if result.get("status") == "success":
            context[f"step_{result['step']}_output"] = result.get("output", {})
    
    # 将最后成功的结果作为主要输入
    for result in reversed(previous_results):
        if result.get("status") == "success":
            output = result.get("output", {})
            if isinstance(output, dict):
                # 提取 data 字段作为主数据
                if "data" in output:
                    context["data"] = output["data"]
                else:
                    context["data"] = output
            break
    
    return context

def execute_plan(plan, global_context=None):
    """执行计划"""
    if not plan or not isinstance(plan, list):
        return {
            "status": "error",
            "message": "InvalidPlan: plan must be a non-empty list"
        }
    
    results = []
    context = global_context.copy() if global_context else {}
    failed_count = 0
    
    for step_info in plan:
        step = step_info.get("step", 1)
        skill = step_info.get("skill", "")
        input_params = step_info.get("input", {})
        
        if not skill:
            results.append({
                "step": step,
                "skill": skill,
                "status": "error",
                "output": None,
                "error": "Empty skill name"
            })
            failed_count += 1
            continue
        
        # 合并上下文到输入
        exec_input = {**context, **input_params}
        
        # 执行技能
        result = execute_skill(skill, exec_input)
        
        results.append({
            "step": step,
            "skill": skill,
            "status": result["status"],
            "output": result.get("output"),
            "error": result.get("error")
        })
        
        if result["status"] == "error":
            failed_count += 1
            # 可以选择继续或停止，这里选择继续执行
            # break  # 如需停止，取消注释
        
        # 更新上下文
        context = build_context(results, global_context)
    
    # 获取最终输出
    final_output = None
    for result in reversed(results):
        if result.get("status") == "success":
            final_output = result.get("output")
            break
    
    return {
        "status": "success" if failed_count == 0 else ("partial" if results else "error"),
        "data": {
            "results": results,
            "final_output": final_output,
            "executed_steps": len(results),
            "failed_steps": failed_count
        }
    }

def execute(params):
    plan = params.get("plan", [])
    context = params.get("context", {})
    
    if not plan:
        return {"status": "error", "message": "InvalidPlan: plan is required"}
    
    return execute_plan(plan, context)

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
python main.py '{"plan": [{"step": 1, "skill": "sou", "input": {"keywords": "test"}}]}'
# Expect: 执行搜技能，返回结果
```

### Multiple Steps
```bash
python main.py '{"plan": [{"step": 1, "skill": "sou", "input": {"keywords": "Python"}}, {"step": 2, "skill": "du", "input": {}}]}'
# Expect: 先搜索，读取结果
```

### Error Handling
```bash
python main.py '{"plan": [{"step": 1, "skill": "nonexistent", "input": {}}]}'
# Expect: {"status": "error", "message": "Skill not found: nonexistent"}
```
