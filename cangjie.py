#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
仓颉造字 - 全局命令行入口
只要会中文，就能编程

安装方法：
1. 把此脚本放到 Python Scripts 目录
2. 或把此项目目录加到 PATH

使用：
    cangjie 搜索Python教程
    cj 写一个计算器
"""

import sys
import os
import json

# 添加项目路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DICT_DIR = os.path.join(SCRIPT_DIR, "skills", "dictionary")

# 如果存在 run.py，则调用它
run_py = os.path.join(DICT_DIR, "run.py")
if os.path.exists(run_py):
    sys.path.insert(0, DICT_DIR)
    from run import auto_execute
    from delivery import deliver

    if __name__ == "__main__":
        # 获取需求参数
        requirement = " ".join(sys.argv[1:])

        if not requirement:
            print("仓颉造字 - 只要会中文，就能编程")
            print("")
            print("用法:")
            print("  cangjie <中文需求>")
            print("")
            print("示例:")
            print("  cangjie 搜索Python教程")
            print("  cangjie 写一个计算器并运行")
            print("  cangjie 读取 https://example.com")
            sys.exit(0)

        # 执行
        result = auto_execute(requirement)

        # 交付
        final_status = result.get("status", "error")
        final_result = result.get("result")
        delivery = deliver(requirement, final_result or result, final_status)

        print(json.dumps(delivery, ensure_ascii=False, indent=2))
else:
    print("错误：找不到仓颉造字计划核心文件")
    print(f"请确认 {DICT_DIR}/run.py 存在")
    sys.exit(1)
