# SFC 对 AI 风险管理提出了哪些要求？

**本库以 24EC55《Use of generative AI language models》为主线。** 它涉及受规管活动中的 AI 语言模型风险；26EC32 补充 AI 网络风险。其他文件放在辅助资料，不作为同等重要的入门要求。

> 内容整理：2026-10-06。原文查阅状态见[来源登记册](../source-register.csv)。

## 先分清文件的作用

| 文件 | 在本库中的作用 | 阅读入口 |
|---|---|---|
| **24EC55：生成式 AI 语言模型** | **核心**。模型验证、客户输出、数据安全、第三方风险等 | [条款导读](24EC55.md) · [速查](../cheatsheets/24EC55.md) |
| **26EC32：网络安全措施** | **补充**。AI 增强攻击、不可信输入和 Agent 权限等相关风险 | [条款导读](26EC32.md) |
| 26EC35：互联网交易认证与监测 | **相关背景**。专项适用范围，不是所有 AI 用例的统一规范 | [适用范围和原文](26EC35.md) |
| 26EC11：GenA.I. Sandbox++ | **沙盒背景**。参与安排，不是通用 AI 控制清单或豁免 | [安排说明](26EC11.md) |

需要判断文件是否适用时，查看[适用范围](applicability.md)。

## 核心要求对应哪些知识？

下表是 `[监管要求/期望]` 的阅读摘要，保留具体条款的适用条件；方法和软件是本库的参考资料，不是 SFC 指定方案。完整条件请读[24EC55 条款导读](24EC55.md)及[官方原文](https://apps.sfc.hk/edistributionWeb/api/circular/openFile?lang=EN&refNo=24EC55)。

| 24EC55 原文定位 | 需要理解的要求 | 本库解释与方法 |
|---|---|---|
| 第13(b)段 | 采用前及重大改变时适当验证，涵盖有关网络及数据控制 | [评估基础](../concepts/evaluation-foundations.md)、[变更回归](../methods/change-regression.md) |
| 第13(c)段 | 从用户输入到系统输出作端到端测试，包括相关组件 | [系统构成](../concepts/system-components.md)、[RAG 检索和生成](../topics/rag.md) |
| 第13(d)段 | 持续检讨与监测表现，确认仍适合用途 | [漂移与监测](../concepts/monitoring-and-drift.md) |
| 第17–19段 | 客户界面披露及高风险用途的额外措施，包括事实性、人审和稳健性 | [输出可靠性](../concepts/output-reliability.md)、[人机交互](../concepts/human-ai-interaction.md) |
| 第20–21段 | 网络风险识别与对抗测试，保留“适当时”和“可行范围”等条件 | [提示注入与安全](../concepts/robustness-and-security.md)、[对抗测试](../methods/adversarial-testing.md) |
| 第22–25段 | 保护非公开资料，关注输入、训练数据及全生命周期机密性 | [数据与隐私](../concepts/data-and-privacy.md)、[隐私测试](../methods/privacy-testing.md) |
| 第26–29段 | 第三方风险、黑盒局限、软件依赖及中断准备 | [第三方与韧性](../concepts/third-party-and-resilience.md) |

原文也包含治理与职责要求，例如第9–12段；本库在[完整导读](24EC55.md)保留定位，但不设计机构治理或审批流程。

## 原文、方法和工具怎样区分？

“第13(c)段要求端到端测试”是原文要求；“分别计算检索召回率和回答事实正确率”是参考方法；“用 Ragas 或 Promptfoo 辅助评估”是工具选项。三者关联，但不能互相替代。

详细来源与解释深度见[原文映射](knowledge-map.csv)。标签说明、解释修正及其他辖区资料放在辅助页面，查到需要时再阅读。
