# 字库 (Character Registry)

这里是存放所有具体 **单字技能 (Character Skills)** 的地方。

## 目录结构

每个单字技能都应该拥有一个独立的子目录，目录名建议使用 **汉字拼音** (如 `sou`, `xie`, `du`)。

```text
characters/
├── sou/                # 【搜】
│   ├── SKILL.md        # 技能定义与元数据
│   ├── main.py         # 执行逻辑
│   └── requirements.txt
├── xie/                # 【写】
│   └── ...
└── ...
```

## 如何添加新字？

1.  在 `characters/` 下创建一个新目录（如 `mychar`）。
2.  参照 `../creation/templates/char_skill_template.md` 编写 `SKILL.md` 和 `main.py`。
3.  确保 `SKILL.md` 包含正确的 Frontmatter 元数据。

## 检索机制

`../retrieval/search_chars.py` 脚本会自动扫描此目录下的所有子文件夹，将其识别为可用的单字技能。
