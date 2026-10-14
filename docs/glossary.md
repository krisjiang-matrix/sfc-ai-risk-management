# AI 风险管理术语与英文别名

> 页面类型：`[技术解释]` · 编写日期：2026-10-05
>
> 通用术语解释用于学习；监管用语及适用边界以[SFC 官方来源](hub/official-sources.md)为准。

这张表适合按中文词或英文别名速查。定义只提供进入主题的简短解释；细节见链接页面，监管含义以官方原文为准。

| 中文 | English terms / aliases | 定义与入口 |
|---|---|---|
| 系统组件 | AI system; foundation model; fine-tuning | 应用可组合模型、提示、检索、过滤、记忆和工具，具体组成视系统而定；微调更新模型参数，RAG 在推理时提供外部资料；[深入阅读](concepts/system-components.md) |
| 幻觉与迎合 | Hallucination; confabulation; sycophancy | 似真但错误的内容，与附和用户而忽略事实的行为；[深入阅读](concepts/output-reliability.md) |
| 过度拒答 | Over-refusal; false refusal | 对应用允许的问题无必要拒答，与越界请求单独计分；[深入阅读](concepts/output-reliability.md) |
| 测试污染 | Test contamination; data leakage | 测试内容用于训练或调参导致乐观评分；[深入阅读](concepts/evaluation-foundations.md) |
| 金标准 | Gold standard; reference labels | 独立可核验的参考答案、证据和允许行为；[深入阅读](methods/gold-standard-design.md) |
| 分层抽样 | Stratified sampling | 按输入类别抽样并说明目标权重；[深入阅读](methods/evaluation-design.md) |
| 模型裁判 | LLM-as-a-judge; model judge | 用模型评判另一模型的输出，须与独立标签校准；[深入阅读](methods/judge-calibration.md) |
| 检索增强生成 | RAG; retrieval-augmented generation | 检索资料后生成答案；分块、召回、重排与整合分别可能出错；[深入阅读](concepts/rag.md) |
| 事实支持 | Groundedness; faithfulness | 声明是否受给定证据支持，不等于证据本身现实正确；[深入阅读](methods/rag-design-diagnostics.md) |
| 召回率 | Recall@k | 前 k 位相关资料数除以全部标注相关资料数；[深入阅读](methods/rag-retrieval-evaluation.md) |
| 检索精确率 | Precision@k | 前 k 位相关资料数除以 k；[深入阅读](methods/rag-retrieval-evaluation.md) |
| 命中率 | Hit Rate@k | 至少命中一条相关资料的问题比例，不等于召回率；[深入阅读](methods/rag-retrieval-evaluation.md) |
| 提示注入 | Prompt injection; indirect injection | 非可信内容被误当系统指令，直接和间接注入位置不同；[深入阅读](concepts/robustness-and-security.md) |
| 越狱与投毒 | Jailbreak; data poisoning; retrieval poisoning | 绕过行为边界，或修改训练/检索资料影响结果；[深入阅读](concepts/robustness-and-security.md) |
| 对抗测试 | Adversarial testing; red teaming | 按威胁模型构造实验并观察实际影响；[深入阅读](methods/adversarial-testing.md) |
| 敏感信息 | PII; personal information | 可能识别个人或其他需保护的内容，须结合上下文；[深入阅读](concepts/data-and-privacy.md) |
| 成员推断 | Membership inference | 推断某记录是否参加训练，并非恢复记录；[深入阅读](methods/privacy-testing.md) |
| 模型反演与提取 | Model inversion; training data extraction | 分别推断数据特征与恢复具体训练内容；[深入阅读](concepts/data-and-privacy.md) |
| 公平性 | Fairness; demographic parity; equalized odds | 多个不同目标和指标，不能化为通用单分数；[深入阅读](concepts/fairness-and-explanation.md) |
| 可解释性 | Explainability; interpretability; counterfactual | 理解因素与证据，推理文本不等于真实内部机制；[深入阅读](methods/fairness-and-explanation.md) |
| Agent | Agentic AI; tool calling | 模型规划并执行工具动作，需观察权限及最终状态；[深入阅读](concepts/agent-risk.md) |
| 幂等性 | Idempotency; idempotency key | 同一请求重试不重复产生副作用；[深入阅读](topics/agent-permissions.md) |
| 数据漂移 | Data drift; covariate shift | 输入分布改变，不等于性能下降；[深入阅读](concepts/monitoring-and-drift.md) |
| 概念漂移 | Concept drift | 输入与正确目标关系变化，需要结果证据；[深入阅读](methods/drift-detection.md) |
| 行为漂移 | Behavior drift; model drift | 同样或相似输入产生不同输出，排查版本和环境；[深入阅读](concepts/monitoring-and-drift.md) |
| 软件物料清单 | SBOM; software bill of materials | 软件依赖清单，不覆盖全部 SaaS 运行依赖；[深入阅读](concepts/third-party-and-resilience.md) |
| 自动化偏差 | Automation bias; over-reliance | 过度相信自动输出并忽略独立证据；[深入阅读](concepts/human-ai-interaction.md) |
