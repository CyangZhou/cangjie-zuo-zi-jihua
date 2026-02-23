#!/usr/bin/env python3
"""
造字工具 - 按文档规范创建单字技能
遵循四大核心要素：IO契约、独立执行，元数据自描述、单元测试

用法:
  python create_char.py <拼音> <汉字> <描述> [标签] [依赖]
  示例: python create_char.py sou 搜 网络搜索 search,web requests
"""

import os
import sys
import json

# 路径设置
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHARS_DIR = os.path.join(BASE_DIR, "characters")
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")


def print_guide():
    """打印造字指南"""
    guide_path = os.path.join(os.path.dirname(__file__), "CREATION_GUIDE.md")
    if os.path.exists(guide_path):
        with open(guide_path, "r", encoding="utf-8") as f:
            content = f.read()
        print("\n=== 造字指南 ===")
        print("核心要素:")
        print("  1. IO Contract - 严格的输入输出契约")
        print("  2. Execution Logic - 独立且幂等的执行逻辑")
        print("  3. Meta-Description - 元数据自描述")
        print("  4. Tests - 单元测试与样例")
        print("\n流程: 定契约 -> 写元数据 -> 实现逻辑 -> 加测试")
        print("=" * 40 + "\n")


def get_template_skill():
    """获取SKILL.md模板"""
    path = os.path.join(TEMPLATE_DIR, "char_skill_template.md")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return None


def create_char(char_name, char_pinyin, description, tags, dependencies):
    """创建单字技能"""
    char_dir = os.path.join(CHARS_DIR, char_pinyin)

    if os.path.exists(char_dir):
        print(f"错误: 单字 '{char_pinyin}' 已存在！")
        return False

    os.makedirs(char_dir)
    print(f"[+] 创建目录: {char_dir}")

    # 1. 生成 SKILL.md
    template = get_template_skill()
    if template:
        skill_md = template.replace("<汉字拼音>", char_pinyin)
        skill_md = skill_md.replace("<汉字>", char_name)
        skill_md = skill_md.replace("<一句话功能描述>", description)
        skill_md = skill_md.replace("<Pinyin>", char_pinyin)
        skill_md = skill_md.replace("[tag1, tag2]", str(tags))
        skill_md = skill_md.replace("[package1, package2]", str(dependencies))

        skill_path = os.path.join(char_dir, "SKILL.md")
        with open(skill_path, "w", encoding="utf-8") as f:
            f.write(skill_md)
        print(f"[+] 创建 SKILL.md")

    # 2. 生成 main.py 框架
    main_py = f'''#!/usr/bin/env python3
"""
{char_name} (单字技能)
{description}
依赖: {dependencies}
"""
import sys
import json

# --- Dependency Self-Check ---
# TODO: 在此添加依赖检查，如：
# try:
#     import requests
# except ImportError:
#     print(json.dumps({{"status": "error", "message": "Missing: pip install requests"}}))
#     sys.exit(1)

# --- Core Logic ---
def execute(params):
    """
    单字执行逻辑
    
    Input Schema:
    {{
        # TODO: 定义输入参数
    }}
    
    Output Schema:
    {{
        "status": "success | error",
        "data": {{ ... }}
    }}
    """
    # TODO: 实现你的逻辑
    return {{"status": "success", "data": {{"result": "ok"}}}}

if __name__ == "__main__":
    try:
        input_str = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
        if not input_str.strip():
            raise ValueError("Empty input")
        params = json.loads(input_str)
        result = execute(params)
        print(json.dumps(result, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({{"status": "error", "message": str(e)}}, ensure_ascii=False))
        sys.exit(1)
'''

    main_path = os.path.join(char_dir, "main.py")
    with open(main_path, "w", encoding="utf-8") as f:
        f.write(main_py)
    print(f"[+] 创建 main.py")

    print(f"\n=== 完成 ===")
    print(f"单字: {char_name} ({char_pinyin})")
    print(f"位置: {char_dir}")
    print(f"下一步: 编辑 SKILL.md 完善 IO Contract, 然后实现 main.py")

    return True


def main():
    print_guide()

    if len(sys.argv) < 3:
        print("用法: python create_char.py <拼音> <汉字> <描述> [标签] [依赖]")
        print("示例: python create_char.py sou 搜 网络搜索 search,web requests")
        return

    char_pinyin = sys.argv[1]
    char_name = sys.argv[2]
    description = sys.argv[3] if len(sys.argv) > 3 else ""
    tags = sys.argv[4].split(",") if len(sys.argv) > 4 else []
    dependencies = sys.argv[5].split(",") if len(sys.argv) > 5 else []

    create_char(char_name, char_pinyin, description, tags, dependencies)


if __name__ == "__main__":
    main()
