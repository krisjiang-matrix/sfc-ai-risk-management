# SFC AI Risk Management Knowledge Base

An open knowledge base that helps risk professionals understand and implement Hong Kong SFC expectations for managing AI risk.

The project connects SFC expectations with the technology behind them: how AI risks arise, how to test system behavior, and where existing tools can help—and what their results do not establish. Readers can start from a requirement or follow a specific question through the relevant concepts, methods and tools.

[Read online](https://krisjiang-matrix.github.io/sfc-ai-risk-management/) · [中文](README.md) · [Browse the knowledge base](docs/en/index.md)

## Why this project exists

SFC circulars set expectations for model validation, data security and third-party risk. Risk professionals also need to understand the technology behind those expectations: why hallucinations occur, how to evaluate RAG, how to test prompt injection, and what a tool's score actually means.

For example: **Why can an AI answer be wrong even when it includes citations?** This project distinguishes missing evidence, outdated sources and unsupported citations, shows how to test each failure, and introduces existing tools such as Ragas and Promptfoo.

## Find what you need

| Question | Entry point |
|---|---|
| What does the SFC expect? | [SFC sources and expectations](docs/regulatory/index.md) |
| What is the risk and how does it arise? | [Risk knowledge](docs/concepts/index.md) |
| How can it be tested or measured? | [Implementation methods](docs/methods/index.md) |
| Which existing software supports the method? | [Tool references](docs/tools/index.md) |

Detailed articles are primarily Chinese; an [English overview](docs/en/index.md) introduces the main topics.

## Scope

Reliability, evaluation, RAG, security, privacy, fairness, agents, drift, third parties, resilience and human–AI interaction. The core source is SFC circular 24EC55 and its appendix, with related AI cyber risk from 26EC32. Known gaps are listed in the [coverage report](docs/coverage.md).

The project explains general knowledge and teaching examples. It does not design institutional governance, approval workflows, forms or new risk tools. Regulatory expectations are separated from optional methods and software.

## Browse locally

Use Python 3.11–3.13. Local validation uses macOS ARM64; CI is configured for Ubuntu with Python 3.11 and 3.12. No model, GPU or API credentials are required.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --require-hashes -r requirements-docs.lock
python -m mkdocs serve
```

On Windows, create the environment with `py -3 -m venv .venv` and activate it with `.venv\Scripts\Activate.ps1`. Dependency ranges are in `requirements-docs.txt`; the lock file fixes direct/transitive versions and download hashes. Rebuild and audit when updating it.

Optional social preview: install `requirements-preview.lock` with `--require-hashes`, then run `python scripts/make_social_preview.py`. Pass `--font /path/to/font.ttf` for a local Chinese font. Missing fonts cause an explicit error; fonts are never downloaded or redistributed.

Open `http://127.0.0.1:8000/`. See [CONTRIBUTING](CONTRIBUTING.md) for checks and contributions.

Content: [CC BY 4.0](LICENSE). Code: [MIT](LICENSE-code). Independent educational material, not an SFC publication or endorsement. Official sources prevail.
