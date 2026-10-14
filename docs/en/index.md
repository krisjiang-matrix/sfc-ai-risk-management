# SFC AI Risk Management Knowledge Base

> Published: 2026-10-05. Page type: knowledge base overview. Source verification status is recorded in the [source register](../source-register.csv).

An open knowledge base that helps risk professionals understand and implement Hong Kong SFC expectations for managing AI risk. It explains what the risks are, how to test and measure them, and which existing tools can help. Detailed pages are currently in Chinese; this English entry point links to the main learning paths.

| Question | Start here |
|---|---|
| Where can a system fail? | [System components](../concepts/system-components.md) |
| What makes an evaluation credible? | [Evaluation foundations](../concepts/evaluation-foundations.md) |
| How do retrieval and generation failures differ? | [RAG topic](../topics/rag.md) |
| How does untrusted content become an instruction? | [Prompt injection](../topics/prompt-injection.md) |
| How do we test tool permissions and repeated actions? | [Agent permissions](../topics/agent-permissions.md) |
| How should a model judge be calibrated? | [Model judges](../topics/model-judge.md) |
| Which software or manual approach supports a method? | [Tool capabilities](../tools/index.md) |

## Core topic summaries

**RAG:** Measure retrieval coverage separately from answer faithfulness and factual accuracy. A real citation may still fail to support a claim. Use the same synthetic questions when comparing versions and separately test access isolation.

**Prompt injection:** Retrieved documents and tool outputs are data, not trusted instructions. Test direct, indirect and multi-turn attacks against each boundary. Record model responses, tool requests, permission decisions and actual effects separately, and check whether normal tasks still complete. A scan with no findings only describes the tested conditions.

**Agents:** Correct text does not imply safe action. Check requested tool, parameter scope, identity, repetitions and resource limits against a synthetic environment. A proposed unauthorised call and a completed unauthorised action are different findings; inspect the execution decision and final state.

**Model judges:** An LLM score is a measurement with bias and uncertainty. Compare against independent human labels, examine false passes and false failures, and test sensitivity to wording and answer order.

## Coverage and reuse

[Coverage and gaps](../coverage.md) distinguishes complete learning units, partial coverage, missing coverage and not-applicable cells. “Complete” does not mean all risk is eliminated. Regulatory expectations, technical extensions and synthetic examples are separated. Governance and institutional workflow design are outside the implementation scope. Content is CC BY 4.0; site scripts are MIT.
