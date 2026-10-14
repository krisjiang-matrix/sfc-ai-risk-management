# MLflow：实验、版本与评测结果怎样关联

评测分数提高后，若无法确认测试集、提示和检索参数是否相同，就难以把变化归因于某次修改。**MLflow 将一次实验的参数、指标和产物关联保存，便于追溯与比较版本。** 它提供记录结构；样本是否代表任务、指标是否正确，以及实验是否实际按配置执行，都需要另行核验。

<div class="article-meta" markdown="1">

核实日期：2026-10-05 · 页面状态：[可选工具/框架] · 维护周期：官方版本与接口重要变化时复核

</div>

## 把配置、指标与产物关联到同一次实验

[技术解释] MLflow 提供实验记录、模型注册与调用链追踪（tracing）能力，可关联提示、模型、检索配置及其评估结果。[官方文档](https://mlflow.org/docs/latest/)

experiment 用于组织相关实验，run 表示一次具体运行记录。参数说明所采用的配置，指标保存数值结果，产物保存需要进一步复核的文件或记录。只有数值而没有样本版本和判据，比较界面只能展示差异，无法解释差异由何而来。

例如提示改动同时伴随资料库更新，正确率变化就混合了两个因素。应尽可能固定其余条件，或明确记录同时变化的项目，并保留逐题配对结果。**可追溯意味着能回到输入和判据检查结论**，不能以存在一条完整 run 记录替代对实验设计的判断。

应用或评估代码依据 tracking URI 指定的记录位置，将参数和指标写入后端存储，并将文件等产物写入产物存储，之后再查询与比较。Tracking server 在本地或远端会改变数据去向；产物可含问题、文档和响应，勿仅因本地 SDK 而假设数据留在本机。核心 Apache-2.0，运行环境和版本由官方发行说明确认；本页未重新核实最新发布版本。

## 记录两组固定合成评测结果

[教学示例] 下例仅保存合成指标，无外部模型调用；本次未安装或运行 MLflow。它不注册未实际记录的模型，也不要求不存在的 CSV 文件。

```python
import mlflow

mlflow.set_tracking_uri('file:./mlruns')
mlflow.set_experiment('synthetic-evaluation')
for run_name, prompt_version, correct, total in [
    ('prompt-v1', 'v1', 87, 100),
    ('prompt-v2', 'v2', 90, 100),
]:
    with mlflow.start_run(run_name=run_name):
        mlflow.log_param('prompt_version', prompt_version)
        mlflow.log_param('test_set_version', 'synthetic-1')
        mlflow.log_metric('correct_count', correct)
        mlflow.log_metric('sample_count', total)
        mlflow.log_metric('accuracy', correct / total)
```

代码从同一合成测试集写入两次记录；由输入计数可得 v1=`87/100=0.87`，v2=`90/100=0.90`。这是代码中的预设数据和算术，不是已运行后读回的 MLflow 输出。先按 [官方安装说明](https://mlflow.org/docs/latest/) 固定软件版本，再执行；该代码示例未实测。run ID 用于关联记录，不要硬编码 experiment ID。查询字段按所选版本的 API 确认。旧 Registry stage 教程不宜作为当前通用做法。

## 版本差异必须连接到逐题变化

[参考方法] 上述同一测试集的合成数值相差 `0.90-0.87=0.03`，即提高 3 个百分点；若三个严重错误新出现，总体更高也不代表风险更低。真实比较要固定裁判、参数、模型及文档版本，并逐题保留配对结果；更换测试集后的指标不可直接视为模型改善。

日志中的参数可以写错，记录完整不等于测试执行正确；注册模型也不代表通过验证。自动质量指标与人工事实核对结合，参见 [评估基础](../concepts/evaluation-foundations.md)。替代是版本化 JSON/CSV 与人工比较，或 [Phoenix](phoenix.md) 的调用链观测。

## 官方文档与许可来源

[MLflow 仓库](https://github.com/mlflow/mlflow) · [Tracking 文档](https://mlflow.org/docs/latest/ml/tracking/) · [许可](https://github.com/mlflow/mlflow/blob/master/LICENSE.txt)
