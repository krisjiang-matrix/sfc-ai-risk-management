# SFC AI 风险管理知识库

这是一个帮助风险管理人员理解和落实香港证监会（SFC）AI 风险管理要求的开源知识库。

这里讲清 **AI 风险是什么、如何检查和衡量、可以用哪些现成工具**。主要读者是风险管理人员；没有技术背景，也可以先从解释和演算例子读起。

> 内容更新：2026-10-06。[English](en/index.md)

## 这个库能帮你做什么

例如，AI 回答带了引用，却仍给出错误结论。这里会解释是漏检了资料、用了过期文件，还是引用没有支持结论；再演示怎样测试这些问题，以及哪些工具能帮助评估。

## 按你的问题阅读

| 你的问题 | 从这里开始 |
|---|---|
| SFC 对 AI 风险管理要求了什么？ | [SFC 要求：先看核心通函与对应知识](regulatory/index.md) |
| AI 为什么会答错？怎样检查事实和引用？ | [输出可靠性](concepts/output-reliability.md) |
| RAG 怎么测？检索和生成有什么区别？ | [RAG](concepts/rag.md) · [完整教学例子](topics/rag.md) |
| 提示注入是什么？防护为什么可能失效？ | [稳健性与安全](concepts/robustness-and-security.md) · [教学例子](topics/prompt-injection.md) |
| 敏感资料会从哪些环节泄漏？ | [数据与隐私](concepts/data-and-privacy.md) |
| Agent 调用工具时可能出什么问题？ | [Agent 风险](concepts/agent-risk.md) · [教学例子](topics/agent-permissions.md) |
| 如何判断评测分数可信？ | [评估基础](concepts/evaluation-foundations.md) · [模型裁判例子](topics/model-judge.md) |
| 系统表现为什么会随时间变化？ | [持续监测与漂移](concepts/monitoring-and-drift.md) |

## 内容怎么组织

**SFC 要求**说明原文要求和适用范围；**风险知识**解释机制；**实现方法**讲测试步骤与演算；**工具参考**介绍现有软件的能力与局限。

每个风险主题会链接到相关方法和工具。你可以直接查一个问题，不必先走完一套阅读流程。

全部风险主题见[风险知识目录](concepts/index.md)，已有方法见[方法目录](methods/index.md)，现有工具见[工具能力表](tools/index.md)。

## 关于这个项目

这是开放的通用知识库，提供解释、方法和教学示例；不替某家机构设计治理、工作流或底稿。教学数字和工具不是 SFC 指定标准。内容采用 CC BY 4.0，独立编写，监管要求以官方文本为准。

[内容覆盖与缺口](coverage.md) · [编辑与贡献说明](editorial/content-standard.md)
