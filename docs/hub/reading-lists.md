# 方法研究与读物

> 核实日期：2026-10-05。已核对以下 arXiv 摘要页的标题、编号与摘要；没有宣称阅读全文或复现实验。

这些论文用于理解评估与技术机制，不作为监管依据。原始研究有实验条件，不能直接外推到金融业务或所有当前模型。

| 原始研究 | 为什么读 | 来源编号 |
|---|---|---|
| [Holistic Evaluation of Language Models](https://arxiv.org/abs/2211.09110) | 多维度评估和公开覆盖缺口，不把单个分数视为模型质量 | source_id: `HELM` |
| [Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena](https://arxiv.org/abs/2306.05685) | 位置、长度、自我偏好及人类偏好评估；不等于金融事实裁判有效 | source_id: `LLM-JUDGE` |
| [Ragas: Automated Evaluation of Retrieval Augmented Generation](https://arxiv.org/abs/2309.15217) | 检索与生成的评估维度；论文与当前软件接口分开核对 | source_id: `RAGAS-PAPER` |
| [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172) | 上下文位置与长文本利用；不是访问控制证明 | source_id: `LOST-MIDDLE` |
| [Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/abs/2212.08073) | 用原则与反馈约束行为；训练对齐不消除所有攻击风险 | source_id: `CONSTITUTIONAL-AI` |

## 与知识库连接

[评估设计](../methods/evaluation-design.md)解释目标分布与不确定性；[裁判校准](../methods/judge-calibration.md)解释评分误差；[RAG](../topics/rag.md)解释检索、生成和引用的不同失效。安全及 Agent 研究优先从[威胁类别](../concepts/robustness-and-security.md)和[权限机制](../concepts/agent-risk.md)建立问题，再补充原始研究。

目前未完成隐私攻击、代理长期任务及跨模态风险的系统文献综述，这些缺口可贡献。关键来源的查阅范围记录在[来源登记](../source-register.csv)。
