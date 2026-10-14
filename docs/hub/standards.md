# 标准与框架地图

> **核实日期**：2026-09-30

> 页面状态: 索引页
>
> 维护周期: 新增标准或工具引用时维护
>
> **本页全部条目均为 `[可选工具/框架]` 或框架参考。** 没有任何一项是 SFC 指定的标准、
> 采购清单或合规认证。本页只回答一个问题：**哪一项标准能支撑本库的哪个方法？**

需要判断 SFC 原文及适用范围时，从[官方文件索引](official-sources.md)和[监管导读](../regulatory/index.md)开始；本页的框架对照用于理解概念和方法，不替代监管文本。

---

## 外部参考与监管依据的关系

1. **信息输入，非合规输出**：外部框架帮助理解概念与设计方法，不能替代监管原文
2. **不声称等同**：不得声称「遵循某框架」即满足 SFC 要求
3. **标注非指定**：提及某框架不构成采购建议或监管认可
4. **版本可追溯**：每个条目记录版本号与访问日期

---

## 风险框架：组织风险与测量问题

面对同一套 AI 系统，可以从模型风险、网络安全或管理体系三个角度组织问题。框架的作用是提供分类和分析结构，使资料缺口更容易识别；它不自动给出机构用例的测试输入、通过标准或监管结论。应先说明分析对象，再选择相应结构。

| 框架 | 发布方 | 版本 | 参考用途 | 官方入口 |
|---|---|---|---|---|
| NIST AI RMF | NIST | 1.0 | AI 风险特征与 Govern/Map/Measure/Manage 四功能结构，用于理解风险分类、测量与管理概念；不编写组织治理实施方案 | <https://www.nist.gov/itl/ai-risk-management-framework> |
| NIST CSF 2.0 | NIST | 2.0 | Govern/Identify/Protect/Detect/Respond/Recover，用于网络安全控制分类 | <https://www.nist.gov/cyberframework> |
| ISO/IEC 42001 | ISO/IEC | 2023 | AI 管理体系（**认证类**，非 SFC 要求） | <https://www.iso.org/standard/81230.html> |
| ISO/IEC 23894 | ISO/IEC | 2023 | AI 风险管理实施指南，风险处置的通用方法 | <https://www.iso.org/standard/77304.html> |
| CSA AI Controls Matrix | Cloud Security Alliance | 持续更新 | AI 控制项与成熟度自评的横向参照 | <https://cloudsecurityalliance.org/> |

详细解读：[NIST AI RMF 与 NIST CSF](../tools/nist-ai-rmf-and-csf.md)

---

## 威胁分类：从风险类别形成具体测试

确定要研究提示注入或数据泄漏后，还须说明攻击从哪里进入、能够触达什么组件，以及什么证据表示失败。威胁分类提供这一拆解的参考，具体用例仍需结合系统边界设计；目录列出的类别不是已经执行的测试。

| 框架 | 发布方 | 版本 | 参考用途 | 官方入口 |
|---|---|---|---|---|
| OWASP Top 10 for LLM & GenAI | OWASP | 持续更新 | LLM 应用风险清单，用于设计对抗测试范围 | <https://genai.owasp.org/> |
| MITRE ATLAS | MITRE | 持续更新 | 对抗性 AI 攻击的战术与技术，用于威胁建模 | <https://atlas.mitre.org/> |

详细解读：[OWASP GenAI Top 10](../tools/owasp-genai.md) · [MITRE ATLAS](../tools/mitre-atlas.md)

!!! note "框架不是测试用例"

    OWASP 与 ATLAS 提供风险类别、攻击技术和参考资料，仍需结合目标系统构造适用用例。仅勾选分类条目不能证明覆盖充分；测试输入、预期行为与结果判据见[对抗测试方法](../methods/adversarial-testing.md)。

---

## 辅助软件：执行、观测与资料处理

测试方案确定后，软件可承担批量运行、自动评分、版本记录或资料识别等工作。这些能力处理的对象不同：评分检查输出，追踪还原过程，组件清单记录依赖。因此应按需要取得的证据选择实现，不能用一个扫描结果代替所有检查。

工具页均为 `[可选工具/框架]`。**提及不构成采购建议，也不代表任何厂商的认可或背书。**

| 工具 | 类别 | 参考用途 | 官方入口 |
|---|---|---|---|
| garak | LLM 漏洞扫描 | 对抗测试与提示注入探测的批量执行 | <https://github.com/NVIDIA/garak> |
| Promptfoo | 提示与断言评测 | 金标准测试集的批量断言与回归 | <https://www.promptfoo.dev/> |
| Azure AI Evaluation SDK | RAG 评估器 | 不同评估器对输入字段要求不同；本库示例只演示人工核对口径，不代表已调用 SDK | <https://learn.microsoft.com/en-us/azure/foundry-classic/how-to/develop/evaluate-sdk> |
| MLflow | 模型追踪 | 版本、指标与工件的关联留痕 | <https://mlflow.org/> |
| Evidently | 数据质量与漂移 | 对比参考集和当前集；分布变化本身不证明模型性能下降 | <https://github.com/evidentlyai/evidently> |
| Presidio | 敏感实体识别 | 检出与脱敏须按实体类型、语言及数据类型复核 | <https://github.com/data-privacy-stack/presidio> |
| Syft | SBOM 生成 | 第三方组件的软件物料清单 | <https://github.com/anchore/syft> |
| Dependency-Track | 供应链管理 | SBOM 导入、组件风险与依赖可视 | <https://dependencytrack.org/> |
| Microsoft Purview | 数据治理 | 训练/检索数据使用与分类的治理侧参考 | <https://learn.microsoft.com/purview/> |
| 现有导出与表格方案 | 无工具方案 | **零采购起步路线**：只读导出 + 人工抽样演算 | 本库页面：[现有导出与表格方案](../tools/existing-exports-and-spreadsheets.md) |

!!! warning "工具输出不是合规结论"

    工具产出的扫描报告、指标数值、红队发现都是**测试证据**，
    不是合规结论，也不自动产生「本用例已受控」的判断。
    从证据到结论的判断由人做出。

---

## 供应链：组件清单与服务恢复的区别

知道系统使用了哪些组件，是分析依赖风险的起点。组件清单有助于核对软件身份和许可，但不能说明服务中断后仍可完成任务；恢复测试则需要实际替代路径、关键状态和结果判据。两种证据应分别取得并关联分析。

| 主题 | 本库方法页 | 相关框架 |
|---|---|---|
| 组件清单与许可风险 | [SBOM 审查](../tools/syft.md) · [Dependency-Track](../tools/dependency-track.md) | Syft / Dependency-Track / OWASP GenAI |
| 供应商准入与持续尽调 | [供应商尽职调查](../concepts/third-party-and-resilience.md) | — |
| 黑盒模型不可尽调时的处置 | [黑盒模型局限性](../concepts/third-party-and-resilience.md) | — |
| 集中度与中断预案 | [集中度与恢复演练](../methods/concentration-and-recovery.md) | NIST CSF Recover / ISO 42001 |
| 退出与替代方案 | [退出路径与回退](../concepts/third-party-and-resilience.md) | — |

---

## 框架结构的比较边界

不同框架的分类层级与目标不同。下表仅提供概念参考，不是官方等价映射，也不能据此认定覆盖其中一列就满足另一列：

| 分析任务 | NIST AI RMF | NIST CSF 2.0 | OWASP / ATLAS |
|---|---|---|---|
| 列出 AI 风险 | Govern / Map 中的风险识别 | Identify 中的资产与风险 | 攻击技术分类 |
| 设计验证 | Measure 功能 | Protect / Detect | 攻击面清单 |
| 设阈值与回测 | Measure 中的指标体系 | Detect 中的监控指标 | — |
| 出事件响应 | Manage（含响应机制） | Respond / Recover | 攻击链溯源 |
| 第三方 | Map / Manage | Identify 供应链 | — |

**概念位置相近，不代表义务、方法或证据等价。** 具体标准答案设计见[金标准方法](../methods/gold-standard-design.md)，软件能力与限制见[工具目录](../tools/index.md)。

---

## 来源版本的可追溯性

| 要求 | 说明 |
|---|---|
| 记录版本号 | 每个引用须记录框架版本（如 NIST AI RMF 1.0、OWASP Top 10 for LLM v2.0） |
| 记录访问日期 | `YYYY-MM-DD` 格式，登记入 [`source-register.csv`](../source-register.csv) |
| 固定提交哈希 | 引用开源工具源码时固定 commit，不用 `main` |
| 标记核实状态 | 已核实 / 已读取页面 / 仅访问入口 / 待核实，四选一，不得留空 |
| 框架更新即复核 | 框架版本更新时重新核对引用概念是否仍适用 |

维护流程见[维护与更新机制](../editorial/maintenance.md)。

---

## 框架资料的贡献要求

1. 提供**官方一手来源**（发布方官网或官方仓库），不接受二手转述
2. 写入 `source-register.csv`，含 `version` 与 `accessed_at`
3. 在本页表格中**说明它支撑本库哪个方法**——说不清就不收
4. 明确标注 `[可选工具/框架]`，**不得**写成监管要求或采购建议
5. 如果它是认证标准（如 ISO/IEC 42001），须说明本库**不主张**认证要求

---

**相关页面**：[15 秒决策图](start-here.md) · [辖区地图](jurisdictions.md) ·
[论文与读物清单](reading-lists.md) · [外部参考资料导读](../references/index.md) ·
[资料复用与知识产权政策](../references/reuse-policy.md)

---

<style>
.md-typeset table:not([class]) { font-size: .78rem; line-height: 1.65; }
</style>
