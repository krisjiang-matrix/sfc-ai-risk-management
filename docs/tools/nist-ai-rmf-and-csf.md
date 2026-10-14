# NIST AI RMF 与 CSF：框架能帮助理解什么

AI 回答失真与软件资产失控属于不同风险，但实际应用中可能同时存在。需要先分清分析对象，再选择适用的测量与验证方法。**NIST AI RMF 提供 AI 风险分析框架，NIST CSF 提供网络安全成果分类。** 两者可作为概念参照，SFC 要求的适用范围与措辞仍须回到通函原文核对。

> **核实日期**：2026-09-30

> 参考: [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) | [NIST CSF](https://www.nist.gov/cyberframework)
>
> 页面状态: `[可选工具/框架]` — 框架参考，非软件产品
>
> 维护周期: 持续关注

本页将 AI RMF 用作理解 AI 风险分类与测量的概念资料，将 CSF 用作网络安全分类参考。两者是框架指南，不是软件，也不是 SFC 指定标准；本库不展开其治理制度、职责或实施流程。SFC 原文及适用范围见[监管导读](../regulatory/index.md)。

本页映射仅依据 NIST AI RMF 1.0 与 CSF 2.0。NIST 的 [AI RMF 页面](https://airc.nist.gov/airmf-resources/airmf/0-ai-rmf-1-0/)注明 1.0 正在修订；本页未把尚未发布的修订内容纳入对照（该页面于 2026-10-08 查阅）。

## AI 风险与网络安全采用不同的分析框架

两个框架均由美国国家标准与技术研究院（NIST）发布，但分析对象不同。AI RMF 关注 AI 系统及使用情境中的风险，CSF 从网络安全成果组织相关问题；两者可同时用于理解一个应用，而不是互相替代。

### AI 风险与网络安全的分析对象

<div class="tool-evidence-table" markdown="1">

| 框架 | 全称 | 分析对象与范围 |
|------|------|---------------|
| **NIST AI RMF 1.0** | Artificial Intelligence Risk Management Framework | 如何系统性地管理 AI 系统的风险——从设计、开发、部署到退役的全生命周期 |
| **NIST CSF 2.0** | Cybersecurity Framework | 如何系统性地管理组织的网络安全风险——识别、保护、检测、响应和恢复 |

</div>

### AI RMF 核心结构

```text
GOVERN（治理）贯穿并影响其他功能

MAP（映射）  ↔  MEASURE（度量）  ↔  MANAGE（管理）
      ↑_____________________________________↓

三项功能可按情境迭代和交叉引用；这不是固定顺序的检查清单。
```

### CSF 核心结构

```text
CSF 2.0 六大功能：
GOVERN · IDENTIFY · PROTECT · DETECT · RESPOND · RECOVER
```

它们按网络安全成果分类，不表示必须依次完成或彼此重要性相同；实际行动随组织和用例而异。见 [NIST CSF 2.0](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=957258)。

NIST 框架可提供概念与方法参考，但**不是 SFC 指定或要求的标准**。框架功能与通函主题可能重叠，义务的具体内容仍以通函为准。以下表格仅用于理解分析角度，不能转化为自动证明合规的检查清单。

### 与 SFC 通函的概念重叠

<div class="tool-evidence-table" markdown="1">

| SFC 通函要求域 | AI RMF 参考功能 | CSF 参考功能 |
|---------------|---------------------|-------------------|
| AI 政策与治理（24EC55 §9–12，来源概念介绍） | GOVERN | GOVERN |
| 相关用例与风险因素识别（24EC55 §5、§7–9；不据此虚构统一台账要求） | MAP | IDENTIFY |
| 模型验证与评测（24EC55 §18-19） | MEASURE | — |
| 数据治理（24EC55） | MAP、MEASURE | PROTECT |
| 网络资产管理（26EC32 §6） | — | IDENTIFY |
| 漏洞管理（26EC32 §9） | — | IDENTIFY、PROTECT |
| 安全监测（26EC32 §12） | — | DETECT |
| 事件响应（26EC32 §14–16；通知另见§18） | — | RESPOND |
| 备份与恢复（26EC32 §17） | — | RECOVER |

</div>

**注意**: 上表仅展示概念层面的重叠；并列功能不表示固定顺序，也不表示 SFC 要求等同或引用 NIST 框架。

## 从监管原文建立有边界的概念对照

概念对照首先要说明比较的对象。例如回答准确性可以从 AI RMF 的有效与可靠特征理解，而网络资产识别可借 CSF 的 IDENTIFY 功能组织问题。这只能解释分析角度相近，不能证明两份来源的义务强度、适用对象和验证要求相同。

对于合成产品问答系统，可以分别提出资料是否有效、回答是否受证据支持、软件依赖是否可见、工具权限是否受到限制等问题，再选择相应测试。框架有助于检查分析维度的遗漏；只有具体样本、配置和结果，才能描述系统在已测条件下的表现。

AI RMF 的可信 AI 特征为可靠性、隐私、公平等问题提供术语参照；CSF 则帮助从资产、防护、检测、响应与恢复等角度理解网络安全。阅读框架后，仍应根据任务重新确定测量对象与判据，不能把分类名称直接作为已完成验证的证据。

进行概念对照时，先理解 SFC 原文的适用对象和具体措辞，再查 NIST 中可供参考的概念，最后说明重叠与差异。不能以“遵循 NIST”作为满足 SFC 要求的结论，也不能在没有独立依据时把 NIST 子类别直接变成监管合规项或审计标准。

## 可信 AI 特征对应不同的评估问题

<div class="tool-evidence-table" markdown="1">

| NIST AI RMF 可信特征 | NIST 描述 | 本知识库相关域 |
|---------------------|-----------|---------------|
| Valid & Reliable（有效与可靠） | 系统在预期条件下持续准确运行 | 模型验证、变更回归测试 |
| Safe（安全） | 系统不危及人类生命、健康、财产或环境 | 对客输出、高风险用例 |
| Secure & Resilient（安全与韧性） | 系统抵御攻击并从中恢复 | 对抗测试、网络安全、供应商恢复 |
| Accountable & Transparent（可问责与透明） | 对系统输出负责并向利益相关者提供信息 | 人审披露、独立检查 |
| Explainable & Interpretable（可解释） | 系统决策的机制和推理可被理解 | 对客解释、管理报告 |
| Privacy-Enhanced（隐私增强） | 保护个人隐私和数据权利 | 数据生命周期、供应商数据使用 |
| Fair（公平） | 管理有害偏差 | 偏差与漂移检测 |

</div>

**注意**: 上表仅供参考，本知识库的具体要求范围和措辞强度与 NIST 框架不同。

## CSF 功能与网络安全通函的概念重叠

<div class="tool-evidence-table" markdown="1">

| CSF 功能 | CSF 2.0 描述 | 26EC32 相关段落 |
|----------|-------------|----------------|
| GOVERN | 建立网络安全治理和策略 | 整体监管期望 |
| IDENTIFY | 识别资产、风险和管理上下文 | §6 资产管理 |
| PROTECT | 实施防护措施 | §9 漏洞管理、§10–11 权限与不可信输入 |
| DETECT | 及时发现网络安全事件 | §12 威胁及异常监测 |
| RESPOND | 对网络安全事件采取行动 | §14–16 响应与测试，§18 通知 |
| RECOVER | 恢复能力和服务 | §17 备份与恢复 |

</div>

**注意**: 上表仅展示 26EC32 段落与 CSF 功能的概念层面对照，不是逐条映射。

## 其他框架的参考性质与来源边界

<div class="tool-evidence-table" markdown="1">

| 标准 | 发布方 | 与本知识库的关系 |
|------|--------|-----------------|
| ISO/IEC 42001 | ISO/IEC | AI 管理体系标准；不是 SFC 要求 |
| ISO/IEC 23894 | ISO/IEC | AI 风险管理指南；不是 SFC 要求 |

</div>

HKMA 指引、PDPO 等监管或法律来源不属于 NIST 的替代框架；按辖区查阅[官方来源索引](../hub/official-sources.md)。

## 官方入口

<div class="tool-evidence-table" markdown="1">

| 资源 | URL | 验证日期 |
|------|-----|---------|
| NIST AI RMF 1.0 | [https://www.nist.gov/itl/ai-risk-management-framework](https://www.nist.gov/itl/ai-risk-management-framework) | 2026-09-30 |
| NIST AI RMF Playbook | [https://airc.nist.gov/AI_RMF_Knowledge_Base/Playbook](https://airc.nist.gov/AI_RMF_Knowledge_Base/Playbook) | 2026-09-30 |
| NIST CSF 2.0 | [https://www.nist.gov/cyberframework](https://www.nist.gov/cyberframework) | 2026-09-30 |
| NIST CSF 2.0 参考工具 | [https://csrc.nist.gov/projects/cprt/catalog](https://csrc.nist.gov/projects/cprt/catalog) | 2026-09-30 |

</div>

---
