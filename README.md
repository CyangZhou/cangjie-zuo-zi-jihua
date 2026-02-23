# 仓颉造字计划

**只要会中文，就能编程。**

让任何会中文的用户，无需学习任何编程语法，仅用自然语言描述需求，AI 就能理解意图、生成代码、自动执行、修复错误，最终交付可用的程序。

---

## 快速开始

```bash
# 克隆项目
git clone https://github.com/CyangZhou/cangjie-zuo-zi-jihua.git
cd cangjie-zuo-zi-jihua

# 运行（推荐方式）
python skills/cangjie/main.py "搜Python教程"

# 或使用内置命令
python cangjie.py "写个计算器"
```

---

## 功能演示

| 输入 | 输出 |
|------|------|
| `搜Python教程` | 搜索结果列表 |
| `写个计算器` | 计算器代码 |
| `写个计算器并运行` | 直接运行计算器，输出结果 |
| `读取 https://example.com` | 网页内容 |

---

## 核心架构

```
用户(中文需求)
    ↓
[dong 懂] 意图识别
    ↓
[ce 策] 制定计划
    ↓
[xing 行] 执行技能链
    ↓
[yan 验] 验证结果
    ↓
[xiu 修] 修复错误
    ↓
用户得到结果 + 指引
```

---

## 技能体系

### 核心5技能
| 技能 | 功能 |
|------|------|
| dong (懂) | 理解中文需求，提取关键信息 |
| ce (策) | 制定执行计划，选择技能组合 |
| xing (行) | 按计划调用技能执行任务 |
| yan (验) | 检查结果是否符合预期 |
| xiu (修) | 自动检测和修复错误 |

### 基础技能
| 技能 | 功能 |
|------|------|
| sou (搜) | 网络搜索 |
| xie (写) | 代码/内容生成 |
| du (读) | 读取URL或文件 |
| cun (存) | 保存内容到文件 |
| yun (运) | 执行代码 |

### 全部技能 (26个)
sou, xie, du, cun, yun, bi, dong, ce, xing, yan, xiu, hua, fa, gai, ji, jian, kong, lian, liu, mu, pei, qu, ting, wen, yi, yun

---

## 项目结构

```
cangjie-zuo-zi-jihua/
├── skills/
│   ├── cangjie/          # 核心入口技能
│   │   ├── SKILL.md       # 技能定义
│   │   └── main.py        # 执行逻辑
│   └── dictionary/        # 完整技能库
│       ├── run.py         # CLI入口
│       ├── delivery.py    # 交付系统
│       ├── memory.py      # 记忆系统
│       ├── evo.py         # 进化系统
│       └── characters/    # 26个单字技能
├── AGENTS.md              # 项目规则
├── EVOLUTION.md           # 进化路线图
└── STRUCTURE.md          # 结构说明
```

---

## 使用方式

### 方式1：直接调用 cangjie 技能

```python
from skills.cangjie.main import execute

result = execute({"requirement": "搜索Python教程"})
print(result)
```

### 方式2：命令行

```bash
cd skills/dictionary
python run.py "搜索Python教程"
```

### 方式3：全局命令

```bash
# 添加到 PATH 后
cangjie "写个计算器"
```

---

## 进阶功能

### 记忆学习
系统会自动记忆成功/失败模式，下次执行相同需求时会参考历史。

### 错误修复
执行失败时自动尝试修复，最多重试5次。

### 中文错误解释
技术错误会自动翻译成通俗中文：
- `FileNotFoundError` → "文件不存在"
- `SyntaxError` → "代码语法有误"

---

## 技术栈

- Python 3.x
- 无外部依赖（纯标准库）
- 支持 Windows / Linux / macOS

---

## 参与贡献

欢迎提交 Issue 和 PR！

---

## 许可证

MIT License
