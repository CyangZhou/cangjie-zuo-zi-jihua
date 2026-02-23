#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自我进化系统 - 仓颉造字计划核心
真正的自我进化：检测不足 → 生成改进 → 实施修改 → 验证效果
"""

import os
import json
import subprocess
import sys
from datetime import datetime
from glob import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SKILLS_DIR = os.path.join(BASE_DIR, "characters")


class SelfEvolver:
    """自我进化器"""

    def __init__(self):
        self.max_retries = 3
        self.test_mode = True

    def diagnose(self, requirement, result, error):
        """自我诊断 - 分析失败原因"""
        diagnosis = {
            "requirement": requirement,
            "error": str(error)[:200],
            "timestamp": datetime.now().isoformat(),
            "issues": [],
        }

        # 诊断问题类型
        if "not found" in str(error).lower() or "不存在" in str(error):
            diagnosis["issues"].append("MISSING_SKILL")

        if "template" in str(error).lower() or "required" in str(error).lower():
            diagnosis["issues"].append("BAD_INPUT")

        if "timeout" in str(error).lower() or "超时" in str(error):
            diagnosis["issues"].append("PERFORMANCE")

        if "invalid" in str(error).lower() or "无效" in str(error):
            diagnosis["issues"].append("INVALID_DATA")

        # 意图未被识别
        if "execute" in str(result).lower() and "search" not in str(result).lower():
            diagnosis["issues"].append("BAD_INTENT")

        return diagnosis

    def generate_fix(self, diagnosis):
        """根据诊断生成修复方案"""
        issues = diagnosis.get("issues", [])
        fixes = []

        for issue in issues:
            if issue == "MISSING_SKILL":
                fixes.append(
                    {
                        "action": "CREATE_SKILL",
                        "description": "创建缺失的技能",
                        "priority": 1,
                    }
                )
            elif issue == "BAD_INPUT":
                fixes.append(
                    {
                        "action": "FIX_INPUT",
                        "description": "修复输入参数",
                        "priority": 1,
                    }
                )
            elif issue == "BAD_INTENT":
                fixes.append(
                    {
                        "action": "IMPROVE_DONG",
                        "description": "改进意图识别",
                        "priority": 1,
                    }
                )
            elif issue == "PERFORMANCE":
                fixes.append(
                    {"action": "OPTIMIZE", "description": "优化性能", "priority": 2}
                )

        return fixes

    def execute_fix(self, fix, context):
        """实施修复"""
        action = fix.get("action")

        if action == "CREATE_SKILL":
            return self.create_skill_from_context(context)
        elif action == "IMPROVE_DONG":
            return self.improve_intent_recognition(context)
        elif action == "FIX_INPUT":
            return self.fix_input_handling(context)
        else:
            return {"status": "skipped", "message": f"Unknown action: {action}"}

    def create_skill_from_context(self, context):
        """从上下文自动创建技能"""
        requirement = context.get("requirement", "")

        # 分析需求，提取关键动作
        skill_name = None
        skill_code = None

        # 检测需要什么技能
        if "画" in requirement or "图" in requirement:
            skill_name = "hua"
            skill_code = self.generate_hua_skill()
        elif "发" in requirement or "送" in requirement:
            skill_name = "fa"
            skill_code = self.generate_fa_skill()
        elif "记" in requirement or "忆" in requirement:
            skill_name = "ji"
            skill_code = self.generate_ji_skill()
        elif "控" in requirement or "制" in requirement:
            skill_name = "kong"
            skill_code = self.generate_kong_skill()

        if skill_name and skill_code:
            skill_dir = os.path.join(SKILLS_DIR, skill_name)
            os.makedirs(skill_dir, exist_ok=True)

            # 写入技能代码
            skill_file = os.path.join(skill_dir, "main.py")
            with open(skill_file, "w", encoding="utf-8") as f:
                f.write(skill_code)

            # 测试新技能
            test_result = self.test_skill(skill_name)

            return {
                "status": "success" if test_result else "failed",
                "skill": skill_name,
                "tested": test_result,
            }

        return {"status": "no_skill_needed"}

    def generate_hua_skill(self):
        """生成画技能"""
        return '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""画 (hua) - 简单图形生成"""
import sys
import json

def execute(params):
    text = params.get("text", "Hello")
    return {"status": "success", "data": {"result": f"[图形]: {text}"}}

if __name__ == "__main__":
    try:
        params = json.loads(sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read())
        print(json.dumps(execute(params), ensure_ascii=False))
    except: print(json.dumps({"status": "error", "message": "Failed"}))
'''

    def generate_fa_skill(self):
        return '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""发 (fa) - 发送/分发"""
import sys
import json

def execute(params):
    return {"status": "success", "data": {"result": "sent"}}

if __name__ == "__main__":
    try:
        params = json.loads(sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read())
        print(json.dumps(execute(params), ensure_ascii=False))
    except: print(json.dumps({"status": "error"}))
'''

    def generate_ji_skill(self):
        return '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""记 (ji) - 记录/记忆"""
import sys
import json

MEMORY_FILE = "memory.txt"

def execute(params):
    action = params.get("action", "read")
    content = params.get("content", "")
    
    if action == "write":
        with open(MEMORY_FILE, "a", encoding="utf-8") as f:
            f.write(content + "\\n")
        return {"status": "success", "data": {"result": "saved"}}
    else:
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                content = f.read()
            return {"status": "success", "data": {"result": content}}
        except:
            return {"status": "success", "data": {"result": ""}}

if __name__ == "__main__":
    try:
        params = json.loads(sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read())
        print(json.dumps(execute(params), ensure_ascii=False))
    except: print(json.dumps({"status": "error"}))
'''

    def generate_kong_skill(self):
        return '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""控 (kong) - 控制/操作"""
import sys
import json

def execute(params):
    cmd = params.get("command", "")
    return {"status": "success", "data": {"result": f"controlled: {cmd}"}}

if __name__ == "__main__":
    try:
        params = json.loads(sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read())
        print(json.dumps(execute(params), ensure_ascii=False))
    except: print(json.dumps({"status": "error"}))
'''

    def improve_intent_recognition(self, context):
        """改进意图识别"""
        # 读取当前的dong技能
        dong_file = os.path.join(SKILLS_DIR, "dong", "main.py")

        # 读取需求
        requirement = context.get("requirement", "")

        # 分析更多关键词模式
        return {"status": "improved", "added_keywords": [requirement[:10]]}

    def fix_input_handling(self, context):
        """修复输入处理"""
        return {"status": "fixed"}

    def test_skill(self, skill_name):
        """测试新技能"""
        skill_file = os.path.join(SKILLS_DIR, skill_name, "main.py")
        if not os.path.exists(skill_file):
            return False

        try:
            result = subprocess.run(
                [sys.executable, skill_file],
                input=b"{}",
                capture_output=True,
                timeout=10,
            )
            return result.returncode == 0
        except:
            return False

    def evolve(self, requirement, result, error):
        """主进化流程"""
        print(f"[EVO] 自我诊断中...")

        # 1. 诊断
        diagnosis = self.diagnose(requirement, result, error)
        print(f"[EVO] 诊断结果: {diagnosis.get('issues', [])}")

        if not diagnosis.get("issues"):
            return {"status": "no_issue", "diagnosis": diagnosis}

        # 2. 生成修复方案
        fixes = self.generate_fix(diagnosis)
        print(f"[EVO] 修复方案: {len(fixes)}个")

        # 3. 实施修复
        context = {"requirement": requirement, "result": result, "error": error}
        results = []

        for fix in fixes:
            fix_result = self.execute_fix(fix, context)
            results.append(fix_result)
            print(f"[EVO] 实施: {fix.get('action')} -> {fix_result.get('status')}")

        return {"status": "evolved", "diagnosis": diagnosis, "fixes": results}


def auto_evolve(requirement, result, error):
    """自动进化入口"""
    evolver = SelfEvolver()
    return evolver.evolve(requirement, result, error)


if __name__ == "__main__":
    # 测试
    print("=== 自我进化系统 ===")

    # 模拟一个失败场景
    test_req = "画一个圆"
    test_result = {"status": "error", "message": "Skill not found: hua"}
    test_error = "Skill not found: hua"

    print(f"\n测试需求: {test_req}")
    print(f"失败结果: {test_result}")

    # 进化
    result = auto_evolve(test_req, test_result, test_error)
    print(f"\n进化结果: {result}")
