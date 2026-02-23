# 仓颉造字计划 - 项目规则

## 终极目标

**只要会中文，就能编程。**

让任何会中文的用户，无需学习任何编程语法，仅用自然语言描述需求，AI 就能理解意图、生成代码、自动执行、修复错误，最终交付可用的程序。

---

## 当前规则

<rule id="云舒-evolution-protocol">
  <name>云舒自进化规则</name>
  <description>
    强制调用字典技能完成任务，并在缺字时自主进化生成新字。
  </description>

  <trigger>
    全程生效。遇到新任务、重复问题、复杂流程时必须触发。
  </trigger>

  <principles>
    <principle name="强制字典">
      所有任务执行前必须先调用字典技能检索现有单字，禁止跳过检索直接写脚本。
    </principle>
    <principle name="自主演化">
      无匹配单字时，立即造字、验证、入库，再继续执行任务。
    </principle>
    <principle name="成语优先与组合执行">
      必须使用现有单字组合成工作流完成任务，能命中成语时优先使用成语执行。
    </principle>
  </principles>

  <workflow>
    <step id="1-检索">
      <action>检索是否已有单字技能</action>
      <tool>python skills/dictionary/retrieval/search_chars.py --name [关键词]</tool>
      <logic>
        找到则使用；未找到则进入“造字”。
      </logic>
    </step>

    <step id="2-造字">
      <action>按字典标准造新字并落库</action>
      <guide>python skills/dictionary/creation/create_char.py</guide>
      <requirements>
        - 名称：单字汉字
        - 路径：skills/dictionary/characters/[拼音]/
        - 契约：严格输入输出 Schema
        - 自检：依赖检查与报错处理
      </requirements>
    </step>

    <step id="3-验证">
      <action>验证新字可用性</action>
      <command>python skills/dictionary/characters/[拼音]/main.py [测试输入]</command>
      <logic>
        通过则使用；失败则修复重测。
      </logic>
    </step>

    <step id="4-组合">
      <action>组合单字形成工作流；可命中成语时优先调用成语</action>
      <guide>python skills/dictionary/workflow/define_workflow.py</guide>
      <output>输出可复用的工作流定义或成语调用</output>
    </step>
  </workflow>
</rule>
