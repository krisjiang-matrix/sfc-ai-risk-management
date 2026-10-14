# 内容覆盖与缺口

> 更新日期：2026-10-05。覆盖状态基于内容审阅，不是工具实测或合规评级。

本页用于查看已收录内容及尚未讲透的部分。初次阅读请从[首页](index.md)选一个风险问题。

每项按“概念 × 方法 × 工具 × 来源”检查。[机器可读矩阵](coverage.csv)记录具体路径、来源与缺口。

## 知识主题深度与监管实施覆盖的区别

**这是知识主题的内容深度矩阵，不是 SFC 全部监管要求的逐条实施矩阵。** 主题来自 24EC55 正文和附录，并结合 26EC32 的相关网络风险；[监管映射](regulatory/knowledge-map.csv)记录主题与原文的关联，但没有对全部条款及条件逐项登记实施覆盖状态。因此不能用主题数、页面数或“完整”项数计算监管要求覆盖率。

当前展开的是模型验证、输出可靠性、RAG、对抗与隐私测试、公平性、Agent 边界、监测、依赖与恢复、人审等技术学习内容。治理与人员职责、验证职能分离、客户披露的组织落实、通知程序、供应商合同及机构应变安排主要保留原文导读，不提供完整实施方案。26EC32 的通用网络控制及组织响应也未全面展开。这些范围选择不意味着相关监管要求不适用。

技术主题内仍有实质缺口：训练数据提取与反演、多模态攻击、特定市场公平性和解释、Agent 生产集成、真实生产纵向漂移，以及替代模型和数据迁移的实测。具体情况见下表。本库目前只能说明已收录哪些知识、提供哪些教学路径，不能据此宣称全面覆盖监管实施或证明机构合规。

## 选定知识主题的内容深度

**完整**：在该单元的声明范围内能解释机制、提供实现/演算和结果局限；工具完整表示资料与能力路径可用，不表示工具已运行。**部分**：只有部分风险或实现路径。**缺失**：暂无内容。**不适用**：明确说明原因；不能以此掩盖缺口。

| 专题 | 概念 | 方法 | 工具 | 来源 | 已知缺口 |
|---|---|---|---|---|---|
| [系统构成与风险路径](concepts/system-components.md) | 完整 | [完整](methods/evaluation-design.md) | [完整](tools/mlflow.md) | 完整 | 不覆盖所有模型架构；实现变化需按具体系统重新追踪 |
| [输出可靠性](concepts/output-reliability.md) | 完整 | [完整](methods/factuality-and-citations.md) | [完整](tools/promptfoo.md) | 完整 | 数值计算与多语言有教学路径；暂无真实模型基准 |
| [评估基础](concepts/evaluation-foundations.md) | 完整 | [完整](methods/evaluation-design.md) | [完整](tools/promptfoo.md) | 完整 | 无生产数据；不提供通用样本量和通过阈值 |
| [RAG 检索与生成](concepts/rag.md) | 完整 | [完整](methods/rag-retrieval-evaluation.md) | [完整](tools/ragas.md) | 完整 | 缺少特定中文文档集、长表格的实测对照 |
| [稳健性与安全](concepts/robustness-and-security.md) | 完整 | [部分](methods/adversarial-testing.md) | [完整](tools/garak.md) | 完整 | 多模态攻击与各模型投毒测试尚无完整教学演算 |
| [数据与隐私](concepts/data-and-privacy.md) | 完整 | [部分](methods/privacy-testing.md) | [部分](tools/presidio.md) | 完整 | PII检测可实现；训练提取及反演缺少完整实验；黑盒训练数据通常未知 |
| [偏差、公平性与解释](concepts/fairness-and-explanation.md) | 完整 | [部分](methods/fairness-and-explanation.md) | [部分](tools/fairlearn.md) | 完整 | 公平性有演算；解释提供人工遮蔽路径，未覆盖专门解释工具和特定法律判断 |
| [Agent 风险](concepts/agent-risk.md) | 完整 | [部分](methods/agent-execution-boundary-test.md) | [部分](tools/pyrit.md) | 完整 | 合成轨迹与边界可复核；未提供各类运行时的生产集成 |
| [持续监测与漂移](concepts/monitoring-and-drift.md) | 完整 | [完整](methods/drift-detection.md) | [完整](tools/evidently.md) | 完整 | 有构成/配对演算，尚无真实生产纵向数据 |
| [第三方与韧性](concepts/third-party-and-resilience.md) | 完整 | [完整](methods/concentration-and-recovery.md) | [部分](tools/syft.md) | 完整 | 软件依赖有工具路径；替代模型效果及数据可迁移性需人工或自有观测验证 |
| [人与 AI 交互](concepts/human-ai-interaction.md) | 完整 | [完整](methods/human-review-challenge.md) | [完整](tools/existing-exports-and-spreadsheets.md) | 完整 | 人工盲测可实现；不外推生产人审效力或提供岗位分工 |

## 范围及学习顺序

先了解[系统构成](concepts/system-components.md)，再读[评估基础](concepts/evaluation-foundations.md)。按风险问题选择其他主题，通过[方法目录](methods/index.md)和[工具目录](tools/index.md)形成完整学习链。

“SFC 相关”不是“所有内容都是监管要求”。[监管映射](regulatory/knowledge-map.csv)分别记录正文、附录与技术延伸。治理及组织流程不展开，但保留来源提示；通用 IT、交易认证和政策新闻仅作为相关背景。

## 优先贡献

完善隐私攻击的实验前提、跨语言和多模态测试、解释方法的证据验证、Agent 运行时差异和工具教学实测。请注明实际验证范围，不将介绍文档升级为通过实验。
