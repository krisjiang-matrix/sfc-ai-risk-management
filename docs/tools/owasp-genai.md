# OWASP GenAI：风险分类怎样连接概念和测试

只有“模型可能不安全”这样的描述，难以形成可验证的测试。需要把风险拆成失效机制，说明输入怎样跨越信任边界、输出怎样进入下游动作。**OWASP GenAI 的风险分类提供这些分析入口，帮助检查场景遗漏并组织阅读。** 分类名称本身不等于漏洞证据，也不规定某个软件必然具有完整覆盖。

<div class="article-meta" markdown="1">

核实日期：2026-10-05 · 页面状态：[可选工具/框架] — 风险知识资料 · 维护周期：官方列表及版本更新时复核

</div>

## 风险分类提供问题入口而非测试结论

[技术解释] OWASP GenAI Security Project 提供 LLM 与生成式 AI 安全资料，Top 10 是其中的风险分类入口。它帮助检查遗漏的风险机制，不是软件测试套件，也不是 SFC 指定标准。官方还提供其他专题；本库聚焦概念、方法及工具，不展开其治理制度或工作流。

## 2025 版类别与本库学习路径

以下名称及编号据 [官方 2025 Top 10 页面](https://genai.owasp.org/llm-top-10/) 核实。旧 2023–24 版的名称与顺序不同，不能将旧列表标为当前版。第三列为本库的**示意阅读导航**，不是 OWASP 对本库内容的认可或完整覆盖映射。

<div class="tool-evidence-table" markdown="1">

| 官方编号 | 官方名称 | 本库学习入口 |
|---|---|---|
| LLM01:2025 | Prompt Injection | [稳健性与安全](../concepts/robustness-and-security.md) |
| LLM02:2025 | Sensitive Information Disclosure | [数据与隐私](../concepts/data-and-privacy.md) |
| LLM03:2025 | Supply Chain | [第三方与韧性](../concepts/third-party-and-resilience.md) |
| LLM04:2025 | Data and Model Poisoning | [数据与隐私](../concepts/data-and-privacy.md)、[安全](../concepts/robustness-and-security.md) |
| LLM05:2025 | Improper Output Handling | [系统构成](../concepts/system-components.md) |
| LLM06:2025 | Excessive Agency | [Agent 风险](../concepts/agent-risk.md) |
| LLM07:2025 | System Prompt Leakage | [稳健性与安全](../concepts/robustness-and-security.md) |
| LLM08:2025 | Vector and Embedding Weaknesses | [RAG](../concepts/rag.md) |
| LLM09:2025 | Misinformation | [输出可靠性](../concepts/output-reliability.md) |
| LLM10:2025 | Unbounded Consumption | [Agent 风险](../concepts/agent-risk.md)、[第三方与韧性](../concepts/third-party-and-resilience.md) |

</div>

编号用于引用分类，不应直接当作具体应用的严重性排序。相同类别在不同权限、数据与使用情境下可能产生不同影响。

## 从失效机制连接观察对象与测试方法

例如一份外部文档诱导模型生成删除数据的请求，至少涉及两个问题：文档中的内容是否被提升为指令，以及生成的请求是否被下游允许执行。前者需要检查提示与上下文处理，后者需要观察参数校验、授权和实际状态变化。只检测响应是否出现危险词，会遗漏这两类机制之间的差异。

因此选择方法前应先明确要观察的结果。事实核对关注声明与证据，权限测试关注动作是否获准，组件扫描关注第三方依赖。它们的输出不能互相替代，工具集中列出也不能证明覆盖已完成。下表说明不同问题如何引出相应方法与能力。

[参考方法] 对每个相关类别问清楚：失效由哪个组件产生、输入前提是什么、怎样观察成功或失败、正常请求可能受到什么影响。一个类别可能需要多种方法，一个测试也可能涉及多个类别。

<div class="tool-evidence-table" markdown="1">

| 示意问题 | 方法路径 | 现有工具及边界 |
|---|---|---|
| 文档中的指令是否改变模型任务？ | [对抗测试](../methods/adversarial-testing.md) | [garak](garak.md)、[Promptfoo](promptfoo.md)、[PyRIT](pyrit.md)；先核实版本、目标接入及实际探针 |
| 模型的工具调用是否越权？ | [Agent 边界测试](../methods/agent-execution-boundary-test.md) | 测试工具沙箱与参数校验；只测回答文本不够 |
| 回答是否引用错误或缺失事实？ | [事实与引用核对](../methods/factuality-and-citations.md) | [Ragas](ragas.md)、[Azure 评估器](azure-rag-evaluators.md)；裁判分数需人工校准 |
| 软件依赖有什么已知弱点？ | [第三方风险知识](../concepts/third-party-and-resilience.md) | [Syft](syft.md)、[Dependency-Track](dependency-track.md)；不覆盖模型或数据投毒 |

</div>

上述路径是示例，不给工具赋予未经实测的“高、中、低”覆盖等级。用工具的实际插件清单、配置和样本结果核对覆盖，不能推断一个工具只覆盖两个 OWASP 类别。

## 同一事件可以跨越多个风险类别

[教学示例] 合成模型输出一段含 SQL 操作的文本。若它仅用于展示，与将它直接传入数据库执行是不同的风险路径。后者需要检查下游参数绑定、允许操作及权限，而不是只判断模型是否说了危险词。

提示注入、输出处理及过度代理可能同时作用于同一个事件；分类计数不等于独立漏洞数。通过已测案例不证明风险全覆盖，Top 10 也不涵盖本库所有可靠性、公平性或人机交互知识。

## 官方来源与资料复用条件

[OWASP GenAI](https://genai.owasp.org/) · [Top 10 官方列表](https://genai.owasp.org/llm-top-10/) · [项目仓库](https://github.com/OWASP/www-project-top-10-for-large-language-model-applications)

官方站点注明除另有说明外内容采用 CC BY-SA 4.0；复用图表或大段文字时遵循对应内容的署名与共享条件。相关资料：[MITRE ATLAS](mitre-atlas.md)、[NIST 框架](nist-ai-rmf-and-csf.md)。

来源登记：source_id: `OWASP-LLM-2025`。
