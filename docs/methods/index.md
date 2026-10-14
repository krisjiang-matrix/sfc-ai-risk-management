# 实现方法目录

> 更新日期：2026-10-08。页面类型：`[参考方法]`。

方法说明输入、前提、实现步骤、演算、结果与局限。教学数字不构成通用阈值，组织流程不在本目录设计。

| 要回答的问题 | 方法 |
|---|---|
| 评估如何抽样与控制误差？ | [评估设计](evaluation-design.md)、[金标准](gold-standard-design.md)、[分层抽样](stratified-sampling.md) |
| 事实与引用如何分别判断？ | [原子事实核验](factuality-and-citations.md)、[提示变体](prompt-variation.md) |
| RAG 哪个环节失败？ | [检索评估](rag-retrieval-evaluation.md)、[生成评估](rag-generation-evaluation.md)、[分层诊断](rag-design-diagnostics.md) |
| 自动评分是否可信？ | [裁判校准](judge-calibration.md) |
| 隐私和安全怎么测？ | [隐私测试](privacy-testing.md)、[对抗测试](adversarial-testing.md)、[Agent 边界](agent-execution-boundary-test.md) |
| 群组偏差与解释如何比较？ | [公平性与解释](fairness-and-explanation.md) |
| 性能变化如何发现与比较？ | [漂移诊断](drift-detection.md)、[变更回归](change-regression.md)、[监测数据质量](kri-data-quality-and-backtesting.md) |
| 人审和备用方案是否有效？ | [人审盲测](human-review-challenge.md)、[集中度与恢复](concentration-and-recovery.md) |
| 现有报告能证明什么？ | [证据解读](read-only-evidence-review.md) |

所有方法都有人工或合成复核路径；使用自动化工具前阅读[工具能力表](../tools/index.md)的数据流和限制。
