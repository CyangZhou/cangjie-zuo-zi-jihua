#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto Engine - Cangjie Plan Core
Realize "Chinese speakers can program" closed loop
"""

import sys
import io

# Fix Windows console encoding
if sys.platform == "win32":
    import codecs

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

import json
import subprocess
import os

# --- Config ---
MAX_LOOPS = 5
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SKILLS = {
    "dong": os.path.join(BASE_DIR, "characters", "dong", "main.py"),
    "ce": os.path.join(BASE_DIR, "characters", "ce", "main.py"),
    "xing": os.path.join(BASE_DIR, "characters", "xing", "main.py"),
    "yan": os.path.join(BASE_DIR, "characters", "yan", "main.py"),
    "xiu": os.path.join(BASE_DIR, "characters", "xiu", "main.py"),
}


def run_skill(skill_name, params):
    """Run single skill"""
    skill_path = SKILLS.get(skill_name)
    if not skill_path or not os.path.isfile(skill_path):
        return {"status": "error", "message": f"Skill not found: {skill_name}"}

    try:
        input_json = json.dumps(params, ensure_ascii=False)

        # Use explicit UTF-8 encoding for subprocess - pass bytes to stdin
        result = subprocess.run(
            [sys.executable, skill_path],
            input=input_json.encode("utf-8"),
            capture_output=True,
            timeout=60,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )

        # Decode output as UTF-8
        stdout = result.stdout.decode("utf-8", errors="replace")
        stderr = result.stderr.decode("utf-8", errors="replace")

        if result.returncode != 0:
            return {"status": "error", "message": stderr or "Execution failed"}

        return json.loads(stdout)
    except Exception as e:
        return {"status": "error", "message": str(e)}


def step_dong(requirement):
    print(f"[Dong] Understanding: {requirement[:30]}...")
    params = {"requirement": requirement}
    return run_skill("dong", params)


def step_ce(intent, entities, constraints):
    print("[Ce] Making plan...")
    return run_skill(
        "ce", {"intent": intent, "entities": entities, "constraints": constraints}
    )


def step_xing(plan, context):
    print(f"[Xing] Executing ({len(plan)} steps)...")
    return run_skill("xing", {"plan": plan, "context": context})


def step_yan(result, expectations):
    print("[Yan] Validating...")
    return run_skill("yan", {"result": result, "expectations": expectations})


def step_xiu(error, plan, attempt):
    print(f"[Xiu] Fixing (attempt {attempt + 1}/{MAX_LOOPS})...")
    return run_skill("xiu", {"error": error, "original_plan": plan, "attempt": attempt})


def auto_execute(requirement, expectations=None):
    """Auto execution loop"""
    if expectations is None:
        expectations = {"status": "success", "has_data": True}

    loop_count = 0
    current_plan = None
    final_result = None

    while loop_count < MAX_LOOPS:
        loop_count += 1
        print(f"\n=== Loop {loop_count}/{MAX_LOOPS} ===")

        # Step 1: Dong
        dong_result = step_dong(requirement)
        if dong_result.get("status") != "success":
            print(f"[FAIL] Dong: {dong_result.get('message')}")
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
        print(f"[OK] intent={intent.get('type')}, entities={len(entities)}")

        # Step 2: Ce
        ce_result = step_ce(intent, entities, constraints)
        if ce_result.get("status") != "success":
            print(f"[FAIL] Ce: {ce_result.get('message')}")
            return {"status": "error", "message": "Failed at Ce", "loops": loop_count}

        plan_data = ce_result.get("data", {})
        current_plan = plan_data.get("plan", [])
        print(f"[OK] plan={len(current_plan)} steps")

        if not current_plan:
            return {"status": "error", "message": "No plan", "loops": loop_count}

        # Step 3: Xing
        xing_result = step_xing(current_plan, {"requirement": requirement})
        xing_status = xing_result.get("status", "error")

        if xing_status == "error":
            error_info = {
                "type": "ExecutionError",
                "message": xing_result.get("message", "Unknown"),
            }
            xiu_result = step_xiu(error_info, current_plan, loop_count - 1)
            xiu_data = xiu_result.get("data", {})

            if xiu_data.get("can_retry") and xiu_data.get("new_plan"):
                current_plan = xiu_data["new_plan"]
                print(f"[RETRY] New plan")
                continue
            else:
                print(f"[FAIL] Cannot fix")
                return {
                    "status": "error",
                    "message": "Failed at Xing",
                    "loops": loop_count,
                }

        # Step 4: Yan
        execution_data = xing_result.get("data", {})
        final_result = execution_data.get("final_output", xing_result)

        yan_result = step_yan(final_result, expectations)
        yan_data = yan_result.get("data", {})

        if yan_data.get("passed"):
            print(f"[SUCCESS] {yan_data.get('summary')}")
            return {"status": "success", "result": final_result, "loops": loop_count}
        else:
            print(f"[FAIL] {yan_data.get('summary')}")
            error_info = {
                "type": "ValidationFailed",
                "message": yan_data.get("summary", "Failed"),
            }
            xiu_result = step_xiu(error_info, current_plan, loop_count - 1)
            xiu_data = xiu_result.get("data", {})

            if xiu_data.get("can_retry") and xiu_data.get("new_plan"):
                current_plan = xiu_data["new_plan"]
                print(f"[RETRY] Adjusted plan")
                continue
            else:
                return {
                    "status": "error",
                    "message": "Validation failed",
                    "result": final_result,
                    "loops": loop_count,
                }

    return {
        "status": "error",
        "message": "Max loops",
        "result": final_result,
        "loops": loop_count,
    }


def main():
    if len(sys.argv) > 1:
        input_str = sys.argv[1]
    else:
        input_str = sys.stdin.read()

    if not input_str.strip():
        print(
            json.dumps(
                {"status": "error", "message": "Usage: python engine.py 'requirement'"}
            )
        )
        sys.exit(1)

    try:
        data = json.loads(input_str)
        requirement = data.get("requirement", "")
        expectations = data.get("expectations")
    except json.JSONDecodeError:
        requirement = input_str.strip()
        expectations = None

    if not requirement:
        print(json.dumps({"status": "error", "message": "Empty requirement"}))
        sys.exit(1)

    result = auto_execute(requirement, expectations)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
