#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
写 (xie) - 代码生成技能
根据中文描述生成可运行的代码
"""

import sys
import json
import re

# --- 代码模板库 ---
CODE_TEMPLATES = {
    "python": {
        "hello": """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
print("Hello, World!")""",
        "function": '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
def function_name(params):
    """函数说明"""
    # TODO: 实现逻辑
    return result''',
        "class": '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class ClassName:
    def __init__(self):
        """初始化"""
        pass
    
    def method(self):
        """方法说明"""
        pass''',
        "web_server": """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Hello, World!")

if __name__ == "__main__":
    server = HTTPServer(("localhost", 8080), Handler)
    print("Server running at http://localhost:8080")
    server.serve_forever()""",
        "api": """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api", methods=["GET"])
def hello():
    return jsonify({"message": "Hello, API!"})

if __name__ == "__main__":
    app.run(debug=True)""",
        "file_read": """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
with open("file.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print(content)""",
        "file_write": """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
content = "Hello, World!"
with open("output.txt", "w", encoding="utf-8") as f:
    f.write(content)""",
        "json": """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
data = {"key": "value"}
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)""",
        "http_request": """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import json
url = "https://api.example.com/data"
try:
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
        print(data)
except Exception as e:
    print(f"Error: {e}")""",
        "list": """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
my_list = [1, 2, 3, 4, 5]
my_list.append(6)
for item in my_list:
    print(item)
filtered = [x for x in my_list if x > 3]
print(filtered)""",
        "dict": """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
my_dict = {"name": "Tom", "age": 25}
my_dict["city"] = "Beijing"
for key, value in my_dict.items():
    print(f"{key}: {value}")
value = my_dict.get("name", "default")""",
        "calculator": """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
def add(a, b): return a + b
def sub(a, b): return a - b
def mul(a, b): return a * b
def div(a, b): return a / b if b != 0 else "Error"

print("=== 计算器 ===")
print("1. 加法  2. 减法  3. 乘法  4. 除法")
choice = input("选择运算: ")
a = float(input("输入第一个数: "))
b = float(input("输入第二个数: "))

if choice == "1": print(f"结果: {add(a,b)}")
elif choice == "2": print(f"结果: {sub(a,b)}")
elif choice == "3": print(f"结果: {mul(a,b)}")
elif choice == "4": print(f"结果: {div(a,b)}")
else: print("无效选择")""",
    },
    "javascript": {
        "hello": 'console.log("Hello, World!");',
        "function": "function functionName(params) {\n    return result;\n}",
        "class": "class ClassName {\n    constructor() {}\n    method() {}\n}",
    },
}


def detect_code_type(description):
    """从描述中检测代码类型"""
    desc = description.lower()

    if "javascript" in desc or "js" in desc or "node" in desc:
        language = "javascript"
    else:
        language = "python"

    if "hello" in desc or "你好" in desc or "世界" in desc:
        code_type = "hello"
    elif "函数" in desc or "function" in desc or "def " in desc:
        code_type = "function"
    elif "类" in desc or "class" in desc:
        code_type = "class"
    elif "网页" in desc or "web" in desc or "服务器" in desc or "server" in desc:
        code_type = "web_server"
    elif "api" in desc or "接口" in desc or "rest" in desc:
        code_type = "api"
    elif "计算" in desc or "calculator" in desc or "运算" in desc:
        code_type = "calculator"
    elif "读" in desc or "读取" in desc or "file" in desc:
        code_type = "file_read"
    elif "写" in desc or "保存" in desc or "write" in desc:
        code_type = "file_write"
    elif "json" in desc:
        code_type = "json"
    elif "网络" in desc or "http" in desc or "请求" in desc:
        code_type = "http_request"
    elif "列表" in desc or "list" in desc or "数组" in desc:
        code_type = "list"
    elif "字典" in desc or "dict" in desc or "对象" in desc:
        code_type = "dict"
    elif "计算" in desc or "calculator" in desc or "运算" in desc:
        code_type = "calculator"
    else:
        code_type = "hello"

    return language, code_type


def generate_code(description):
    language, code_type = detect_code_type(description)
    templates = CODE_TEMPLATES.get(language, {})
    return templates.get(code_type, templates.get("hello", "# Generated code"))


def execute(params):
    description = params.get("description", "")
    text = params.get("text", "")
    full_desc = description or text

    if not full_desc:
        return {"status": "error", "message": "Description required"}

    if (
        "代码" in full_desc
        or "script" in full_desc.lower()
        or "python" in full_desc.lower()
        or "javascript" in full_desc.lower()
        or "写" in full_desc
    ):
        code = generate_code(full_desc)
        return {"status": "success", "data": {"result": code}}

    if "readme" in full_desc.lower() or "文档" in full_desc:
        return {
            "status": "success",
            "data": {"result": f"# {full_desc}\n\nTODO: Add content"},
        }

    code = generate_code(full_desc)
    return {"status": "success", "data": {"result": code}}


if __name__ == "__main__":
    try:
        input_str = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
        if not input_str.strip():
            raise ValueError("Empty input")
        params = json.loads(input_str)
        result = execute(params)
        print(json.dumps(result, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}), file=sys.stderr)
        sys.exit(1)
