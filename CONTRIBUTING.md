# 贡献指南

本库欢迎帮助风险人员理解 AI 风险的贡献：补一个概念、完善一个方法、核实一个工具、修正演算、改进图解或翻译英文重点入口。

## 从缺口开始

先看[知识地图](docs/coverage.md)，选择“部分”或“缺失”的能力。小修可直接提交；较大主题先说明它解决的风险问题与所需来源。不要求贡献者设计机构治理、工作流、表格或新工具。

遵循[编辑规范](docs/editorial/content-standard.md)。概念、方法、工具分别组织，不需要机械填写固定十一节。一个页面应形成清楚的学习问题与知识链。

## 来源与标签

使用监管要求/期望、监管附录示例、技术解释、参考方法、教学示例及可选工具/框架六类标签。监管要求有原文定位；自编合成示例标为教学示例。保留原文条件与措辞强度，不把技术框架写成 SFC 义务。

新增关键来源登记到 `docs/source-register.csv`。访问日期、版本和核实状态如实填写，未运行命令明确写“未实测”。新页面页首有发布日期或来源核实日期；项目改动由版本控制记录，来源版本及核实信息由来源登记册记录。

## 验证

```bash
python scripts/verify_knowledge_base.py
python -m mkdocs build --strict
python -m unittest discover -s tests
```

先构建当前内容，再运行测试，才能检查本次生成站点的跳转、搜索和导航；没有生成站点时，这部分测试会跳过。

演算、工具版本和局限需人工检查；自动校验只能验证结构及部分内容边界，不能证明监管解释正确。

不提交真实客户、交易、生产日志、凭据或内部系统信息。内容采用 CC BY 4.0，代码 MIT；第三方资料只链接、摘要或合规短引，不复制受保护全文。标签保留是编辑要求，不增设 CC BY 4.0 之外的许可限制。

## 审阅时说明

写明风险问题、改动效果、核实过哪些来源、做过哪些检查，以及仍有哪些缺口。优先看内容正确与教学价值，不要求页数增长。

通过 [GitHub 仓库](https://github.com/krisjiang-matrix/sfc-ai-risk-management) 的 issue/PR 功能贡献；站点为 [默认项目 Pages](https://krisjiang-matrix.github.io/sfc-ai-risk-management/)。

## 依赖升级

依赖范围分别见 `requirements-docs.txt` 与 `requirements-preview.txt`。使用 uv 更新锁文件：

```bash
uv pip compile requirements-docs.txt --python-version 3.11 --universal --generate-hashes -o requirements-docs.lock
uv pip compile requirements-preview.txt --python-version 3.11 --universal --generate-hashes -o requirements-preview.lock
```

两份锁文件的共有依赖应保持相同版本；升级后用 `--require-hashes` 在干净环境安装，复跑严格构建、回归测试和完整依赖漏洞审计。Actions 使用官方固定提交；升级前核查对应提交的运行时依赖与嵌套引用，不以官方 Security 页面无公告代替依赖审计。
