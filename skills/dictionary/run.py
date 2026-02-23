#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动推进引擎 - 仓颉造字计划核心
实现"只要会中文，就能编程"的完整闭环

功能：
1. 一句话自动执行
2. 技能链自动组合
3. 错误自动修复
4. 自我学习优化
"""

import sys
import json
import subprocess
import os

# --- 自我学习模块 ---
try:
    from memory import learn_success, learn_failure, get_suggested_skills

    HAS_MEMORY = True
except ImportError:
    HAS_MEMORY = False

    def learn_success(*args, **kwargs):
        pass

    def learn_failure(*args, **kwargs):
        pass

    def get_suggested_skills(*args, **kwargs):
        return None


# --- 交付模块 ---
try:
    from delivery import deliver, explain_error, format_result, generate_guide

    HAS_DELIVERY = True
except ImportError:
    HAS_DELIVERY = False

    def deliver(*args, **kwargs):
        return args[1] if len(args) > 1 else {}

    def explain_error(*args, **kwargs):
        return {
            "status": "success",
            "data": {"chinese": "出了点问题", "suggestion": "请重试"},
        }

    def format_result(*args, **kwargs):
        return {"status": "success", "data": {"display": str(args[0]) if args else ""}}

    def generate_guide(*args, **kwargs):
        return {"status": "success", "data": {"guides": []}}


# --- 配置 ---
MAX_LOOPS = 5
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SKILLS = {
    "dong": os.path.join(BASE_DIR, "characters", "dong", "main.py"),
    "ce": os.path.join(BASE_DIR, "characters", "ce", "main.py"),
    "xing": os.path.join(BASE_DIR, "characters", "xing", "main.py"),
    "yan": os.path.join(BASE_DIR, "characters", "yan", "main.py"),
    "xiu": os.path.join(BASE_DIR, "characters", "xiu", "main.py"),
    # 基础技能
    "sou": os.path.join(BASE_DIR, "characters", "sou", "main.py"),
    "xie": os.path.join(BASE_DIR, "characters", "xie", "main.py"),
    "du": os.path.join(BASE_DIR, "characters", "du", "main.py"),
    "cun": os.path.join(BASE_DIR, "characters", "cun", "main.py"),
    "bi": os.path.join(BASE_DIR, "characters", "bi", "main.py"),
    "yun": os.path.join(BASE_DIR, "characters", "yun", "main.py"),
}


def run_skill(skill_name, params):
    """运行单个技能"""
    skill_path = SKILLS.get(skill_name)
    if not skill_path or not os.path.isfile(skill_path):
        return {"status": "error", "message": f"Skill not found: {skill_name}"}

    try:
        input_json = json.dumps(params, ensure_ascii=False)

        result = subprocess.run(
            [sys.executable, skill_path],
            input=input_json.encode("utf-8"),
            capture_output=True,
            timeout=60,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )

        stdout = result.stdout.decode("utf-8", errors="replace")

        if result.returncode != 0:
            return {"status": "error", "message": stdout or "Execution failed"}

        return json.loads(stdout)
    except Exception as e:
        return {"status": "error", "message": str(e)}


def detect_complex_intent(requirement):
    """检测复杂意图，自动组合技能链"""
    req = requirement

    # 检测需要多步骤的场景
    has_search = "搜" in req or "索" in req or "找" in req
    has_read = "读" in req or "看" in req or "打开" in req
    has_write = "写" in req or "生成" in req or "创建" in req
    has_save = "保存" in req or "存" in req or "写入" in req
    has_run = "运" in req or "行" in req or "跑" in req or "编" in req or "程" in req
    has_compare = "比" in req or "比较" in req or "对比" in req or "分析" in req

    # 返回技能链 - 运行优先于单纯写作
    chain = []
    if has_compare:
        chain = ["bi"]
    elif has_search and has_save:
        chain = ["sou", "cun"]
    elif has_search and has_read:
        chain = ["sou", "du"]
    elif has_write and has_run:
        chain = ["xie", "yun"]  # 生成代码并运行
    elif has_write and has_save:
        chain = ["xie", "cun"]
    elif has_search:
        chain = ["sou"]  # 仅搜索
    elif has_write:
        chain = ["xie"]  # 仅写作
    elif has_read:
        chain = ["du"]
    elif has_compare:
        chain = ["bi"]
    elif "画" in req or "图" in req:
        chain = ["hua"]
    elif has_run:
        chain = ["xie", "yun"]  # 生成代码并运行
    elif "发" in req or "送" in req:
        chain = ["fa"]  # 需要自动创建
    elif "记" in req or "忆" in req:
        chain = ["ji"]  # 需要自动创建
    elif "控" in req or "制" in req:
        chain = ["kong"]  # 需要自动创建
    else:
        chain = ["sou"]  # 默认搜索

    return chain


def smart_plan(intent, entities, constraints, requirement):
    """智能制定计划"""
    # 首先尝试从历史中学习 - 如果有相似的成功案例，直接使用
    if HAS_MEMORY:
        suggested_skills = get_suggested_skills(requirement)
        if suggested_skills:
            print(f"[MEMORY] 使用历史成功模式: {suggested_skills}")
            # 从历史技能链构建计划
            plan = []
            for i, skill in enumerate(suggested_skills, 1):
                auto_input = {}
                if skill == "sou":
                    keywords = (
                        requirement.replace("搜索", "").replace("查找", "").strip()
                    )
                    auto_input = {"keywords": keywords or requirement}
                elif skill == "xie":
                    auto_input = {"description": requirement, "text": requirement}
                elif skill == "du":
                    if entities:
                        for e in entities:
                            if e.get("type") in ["file", "url"]:
                                auto_input = {"source": e.get("value", "")}
                                break
                elif skill == "cun":
                    auto_input = {"content": "${data}", "path": "output.txt"}
                elif skill == "yun":
                    auto_input = {
                        "code": "__FROM_CONTEXT_DATA_RESULT__",
                        "language": "python",
                    }
                plan.append(
                    {
                        "step": i,
                        "skill": skill,
                        "input": auto_input,
                        "reason": f"History: {skill}",
                    }
                )
            return plan

    # 其次尝试检测复杂意图
    skill_chain = detect_complex_intent(requirement)

    if skill_chain:
        plan = []
        for i, skill in enumerate(skill_chain, 1):
            auto_input = {}
            if skill == "sou":
                # 提取搜索关键词
                keywords = requirement.replace("搜索", "").replace("查找", "").strip()
                auto_input = {"keywords": keywords or requirement}
            elif skill == "xie":
                auto_input = {"description": requirement, "text": requirement}
            elif skill == "du":
                # 从实体中提取文件/URL
                if entities:
                    for e in entities:
                        if e.get("type") in ["file", "url"]:
                            auto_input = {"source": e.get("value", "")}
                            break
            elif skill == "cun":
                # 自动生成保存路径
                auto_input = {"content": "${data}", "path": "output.txt"}
            elif skill == "yun":
                # 运行代码 - 从上一步(xie)的输出获取代码
                # xie输出在 data.result 中
                # 使用特殊标记，让xing执行时从context获取
                auto_input = {
                    "code": "__FROM_CONTEXT_DATA_RESULT__",
                    "language": "python",
                }
            elif skill == "bi":
                auto_input = {"action": "compare", "text1": requirement, "text2": ""}

            plan.append(
                {
                    "step": i,
                    "skill": skill,
                    "input": auto_input,
                    "reason": f"Complex intent: {skill}",
                }
            )
        return plan

    # 回退到原有的策技能
    ce_result = run_skill(
        "ce", {"intent": intent, "entities": entities, "constraints": constraints}
    )

    if ce_result.get("status") == "success":
        return ce_result.get("data", {}).get("plan", [])

    return []


def auto_execute(requirement, expectations=None):
    """自动执行闭环"""
    if expectations is None:
        expectations = {"status": "success", "has_data": True}

    loop_count = 0
    current_plan = None
    final_result = None

    while loop_count < MAX_LOOPS:
        loop_count += 1
        print(f"\n=== Loop {loop_count}/{MAX_LOOPS} ===")

        # Step 1: Dong
        dong_result = run_skill("dong", {"requirement": requirement})
        if dong_result.get("status") != "success":
            print(f"[FAIL] Dong: {dong_result.get('message')}")
            # 记忆失败模式
            if HAS_MEMORY:
                learn_failure(
                    requirement, {"type": "dong_failed"}, [], dong_result.get("message")
                )
            return {"status": "error", "message": "Failed at Dong", "loops": loop_count}

        intent_data = dong_result.get("data", {})
        if not isinstance(intent_data, dict):
            intent_data = {
                "intent": {"type": "execute"},
                "entities": [],
                "constraints": {},
            }

        intent = intent_data.get("intent", {})
        entities = intent_data.get("entities", [])
        constraints = intent_data.get("constraints", {})
        print(f"[OK] intent={intent.get('type')}")

        # Step 2: Smart Plan
        current_plan = smart_plan(intent, entities, constraints, requirement)
        print(
            f"[OK] plan={len(current_plan)} steps: {[s['skill'] for s in current_plan]}"
        )

        if not current_plan:
            # 记忆失败模式
            if HAS_MEMORY:
                learn_failure(requirement, intent, [], "No plan generated")
            return {
                "status": "error",
                "message": "No plan generated",
                "loops": loop_count,
            }

        # Step 3: Xing
        xing_result = run_skill(
            "xing", {"plan": current_plan, "context": {"requirement": requirement}}
        )
        xing_status = xing_result.get("status", "error")

        # Step 4: Check execution results
        execution_data = xing_result.get("data", {})
        final_output = execution_data.get("final_output", xing_result)

        # 检查最终输出是否有错误（代码执行失败）
        if isinstance(final_output, dict) and final_output.get("status") == "error":
            # 提取错误信息和代码
            error_data = final_output.get("data", {})
            error_msg = error_data.get("error", "")

            # 从当前计划中提取代码
            original_code = ""
            for step in current_plan:
                if step.get("skill") == "yun":
                    original_code = step.get("input", {}).get("code", "")
                    break

            # 获取修复后的代码
            error_info = {
                "type": "ExecutionError",
                "message": error_msg,
                "code": original_code,  # 传递给xiu用于修复
            }
            fixed_code = None
            xiu_result = run_skill(
                "xiu",
                {
                    "error": error_info,
                    "original_plan": current_plan,
                    "attempt": loop_count - 1,
                },
            )
            xiu_data = xiu_result.get("data", {})
            fixed_code = xiu_data.get("fixed_code")

            if xiu_data.get("can_retry"):
                if fixed_code:
                    # 直接使用修复后的代码，跳过xie
                    current_plan = [
                        {
                            "step": 1,
                            "skill": "yun",
                            "input": {"code": fixed_code, "language": "python"},
                            "reason": "使用修复后的代码",
                        }
                    ]
                    print(
                        f"[RETRY] Fixed: {xiu_data.get('suggested_fix', 'Auto-repaired')[:50]}"
                    )
                    continue
                elif xiu_data.get("new_plan"):
                    current_plan = xiu_data["new_plan"]
                    print(f"[RETRY] Adjusted plan")
                    continue
                else:
                    print(
                        f"[WARN] Can retry but no fix: {xiu_data.get('suggested_fix', '')[:50]}"
                    )

        yan_result = run_skill(
            "yan", {"result": final_output, "expectations": expectations}
        )
        yan_data = yan_result.get("data", {})

        if yan_data.get("passed"):
            print(f"[SUCCESS] {yan_data.get('summary')}")
            # 记忆成功模式
            if HAS_MEMORY and current_plan:
                learn_success(requirement, intent, current_plan, final_output)
            return {"status": "success", "result": final_result, "loops": loop_count}
        else:
            print(f"[FAIL] {yan_data.get('summary')}")
            error_info = {
                "type": "ValidationFailed",
                "message": yan_data.get("summary", "Failed"),
            }
            xiu_result = run_skill(
                "xiu",
                {
                    "error": error_info,
                    "original_plan": current_plan,
                    "attempt": loop_count - 1,
                },
            )
            xiu_data = xiu_result.get("data", {})

            if xiu_data.get("can_retry"):
                # 检查是否有修复后的代码或新计划
                fixed_code = xiu_data.get("fixed_code")
                if fixed_code:
                    current_plan = [
                        {
                            "step": 1,
                            "skill": "yun",
                            "input": {"code": fixed_code, "language": "python"},
                            "reason": "使用修复后的代码",
                        }
                    ]
                    print(
                        f"[RETRY] Fixed: {xiu_data.get('suggested_fix', 'Auto-repaired')[:50]}"
                    )
                elif xiu_data.get("new_plan"):
                    current_plan = xiu_data["new_plan"]
                    print(f"[RETRY] Adjusted plan")
                else:
                    print(f"[WARN] Can retry but no fix")
                continue
            else:
                print(f"[FAIL] Cannot validate")
                # 记忆失败模式
                if HAS_MEMORY and current_plan:
                    learn_failure(
                        requirement,
                        intent,
                        current_plan,
                        yan_data.get("summary", "Validation failed"),
                    )
                # 调用自我进化系统
                print(f"[EVO] 尝试自我进化...")
                try:
                    from evo import auto_evolve

                    evo_result = auto_evolve(
                        requirement,
                        final_result,
                        yan_data.get("summary", "Validation failed"),
                    )
                    print(f"[EVO] 进化结果: {evo_result.get('status')}")
                except Exception as e:
                    print(f"[EVO] 进化失败: {e}")

                return {
                    "status": "error",
                    "message": "Validation failed",
                    "result": final_result,
                    "loops": loop_count,
                }

    # 记忆失败模式 - 超过最大循环
    if HAS_MEMORY and current_plan:
        learn_failure(requirement, intent, current_plan, "Max loops exceeded")
    return {
        "status": "error",
        "message": "Max loops",
        "result": final_result,
        "loops": loop_count,
    }


def main():
    """CLI入口"""
    if len(sys.argv) > 1:
        # 直接从命令行获取需求
        requirement = " ".join(sys.argv[1:])
    else:
        # 从stdin读取
        requirement = sys.stdin.read().strip()

    if not requirement:
        print(
            json.dumps(
                {
                    "status": "error",
                    "message": "用法: python run.py <中文需求>\n例如: python run.py 搜索Python教程",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        sys.exit(1)

    print(f"[执行] {requirement}")
    result = auto_execute(requirement)

    # 使用交付系统处理结果
    if HAS_DELIVERY:
        final_status = result.get("status", "error")
        final_result = result.get("result")
        delivery = deliver(requirement, final_result or result, final_status)
        print(json.dumps(delivery, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
