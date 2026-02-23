# 仓颉 (cangjie)

**只要会中文，就能编程。**

## 简介

cangjie 是一个AI编程技能，让AI能直接理解中文需求并执行任务。用户无需学习任何编程语法，只需用自然语言描述需求，AI就能自动完成。

## 功能

- **搜索** - 搜Python教程 → 返回搜索结果
- **写作** - 写个计算器 → 生成代码
- **运行** - 写个计算器并运行 → 直接输出结果
- **读取** - 读取 https://example.com → 返回网页内容
- **保存** - 保存内容到文件

## 使用方式

### 命令行

```bash
python skills/cangjie/main.py "搜Python教程"
python skills/cangjie/main.py "写个计算器并运行"
```

### Python调用

```python
from skills.cangjie.main import execute

result = execute({"requirement": "搜索Python教程"})
print(result)
```

## IO Contract

### Input Schema
```json
{
  "requirement": "string (中文需求描述，必填)"
}
```

### Output Schema
```json
{
  "status": "success | error",
  "data": {
    "requirement": "原始需求",
    "chain": ["执行的技能链"],
    "result": "执行结果"
  },
  "display": "可视化展示",
  "explanation": "执行说明"
}
```

## 意图识别

| 需求示例 | 执行的技能链 |
|----------|-------------|
| 搜Python教程 | sou (搜索) |
| 写个计算器 | xie (写作) |
| 写个计算器并运行 | xie + yun (写作+运行) |
| 搜AI新闻并保存 | sou + cun (搜索+保存) |
| 读取 https://x.com | du (读取) |

## 技能链说明

- `sou` - 搜索技能，调用百度搜索
- `xie` - 写作技能，生成代码（内置hello、calculator等模板）
- `yun` - 运行技能，执行Python代码
- `du` - 读取技能，读取URL或文件
- `cun` - 保存技能，保存到文件

## 错误处理

- 自动重试（最多5次）
- 技术错误自动翻译为中文
- 返回操作指引
