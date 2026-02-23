---
name: dictionary
description: 字典技能 - 仓颉造字体系的核心索引与指南。负责定义单字技能、指导造字、组合工作流、检索现有技能及定义成语。
---
# 字典 (Dictionary)

**Description:**
“字典”是仓颉造字技术的核心元技能。它不仅仅是一个查阅工具，更是整个造字体系的“宪法”和“生成器”。

它具备以下核心能力：
1.  **造字指南 (Creation)**: 定义什么是单字技能，并提供标准模板。
2.  **组合法则 (Workflow)**: 指导如何将单字技能串联成工作流。
3.  **渐进检索 (Retrieval)**: 提供三层结构的检索能力（索引->摘要->详情），高效查找现有技能。
4.  **成语定义 (Idioms)**: 定义封装了复杂逻辑的“成语”工作流。

## Usage

### 1. 获取造字指南 (Create Character)
获取单字技能的定义和创建模板。
```bash
python .trae/skills/dictionary/creation/create_char.py
```

### 2. 获取组合指南 (Define Workflow)
学习如何将单字技能组合成工作流。
```bash
python .trae/skills/dictionary/workflow/define_workflow.py
```

### 3. 检索单字技能 (Search Characters)
使用三层结构检索现有的单字技能。

- **Layer 1: 索引 (Index)** - 列出所有技能名称
  ```bash
  python .trae/skills/dictionary/retrieval/search_chars.py
  ```

- **Layer 2: 摘要 (Summary)** - 查看特定技能的简介
  ```bash
  python .trae/skills/dictionary/retrieval/search_chars.py --name <char_name>
  ```

- **Layer 3: 详情 (Detail)** - 查看特定技能的完整定义
  ```bash
  python .trae/skills/dictionary/retrieval/search_chars.py --name <char_name> --detail
  ```

### 4. 获取成语指南 (Define Idiom)
了解成语工作流的概念和定义方式。
```bash
python .trae/skills/dictionary/idioms/define_idiom.py
```

## File Structure
- `creation/`: 造字相关 (指南 + 模板)
- `workflow/`: 组合相关 (指南)
- `retrieval/`: 检索相关 (脚本 + 指南)
- `idioms/`: 成语相关 (指南)
- `characters/`: 存放具体单字技能的目录 (Registry)
