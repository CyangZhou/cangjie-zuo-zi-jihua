---
name: xie
description: 纯Python文本模板生成
tags: [write, template, generate]
dependencies: []
五行: 木
---

# 写 (Character: xie)

## 1. IO Contract

### Input Schema
```json
{
  "template": "string (模板名：email/title/paragraph/list/code/comment/json)",
  "content": "object (模板所需内容)"
}
```

### Output Schema
```json
{
  "status": "success | error",
  "data": {
    "result": "string"
  }
}
```

## 2. Implementation
```python
import sys
import json

TEMPLATES = {
    "email": lambda c: f"Subject: {c.get('subject', '')}\n\nDear {c.get('name', 'Sir/Madam')},\n\n{c.get('body', '')}\n\nBest regards,\n{c.get('from', 'Sender')}",
    
    "title": lambda c: c.get('text', '').title(),
    
    "paragraph": lambda c: c.get('text', '').strip(),
    
    "list": lambda c: "\n".join(f"- {item}" for item in c.get('items', [])),
    
    "code": lambda c: f"```{c.get('language', 'python')}\n{c.get('code', '')}\n```",
    
    "comment": lambda c: f"# {c.get('text', '')}" if c.get('language', 'python') == 'python' else f"<!-- {c.get('text', '')} -->",
    
    "json": lambda c: json.dumps(c.get('data', {}), ensure_ascii=False, indent=2),
}

def execute(params):
    template = params.get("template", "").strip()
    content = params.get("content", {})
    
    if not template:
        return {"status": "error", "message": "Template name required"}
    
    if template not in TEMPLATES:
        return {"status": "error", "message": f"Unknown template: {template}"}
    
    try:
        result = TEMPLATES[template](content)
        return {"status": "success", "data": {"result": result}}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    try:
        params = json.loads(sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read())
        print(json.dumps(execute(params), ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)
```

## 3. Tests
```bash
python main.py '{"template": "email", "content": {"subject": "Hello", "name": "Tom", "body": "Test"}}'
python main.py '{"template": "list", "content": {"items": ["a", "b", "c"]}}'
```
