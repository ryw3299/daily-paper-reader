<div class="dpr-topic-result-actions"><button type="button" data-topic-copy="docs/starter-pack/20261122-f7bf6220a719/papers.md">复制论文清单</button> <a href="docs/starter-pack/20261122-f7bf6220a719/papers.md" download data-no-router>下载 Markdown</a> <a href="docs/starter-pack/20261122-f7bf6220a719/papers.json" download data-no-router>下载 JSON</a> <button type="button" data-topic-continue="20261122-f7bf6220a719">继续生成阅读内容</button></div>

# car-ai-agent · 入门导读

> 本导读基于所列论文的标题、摘要和已有速览，不代表已阅读全部全文。近期窗口不是完整领域史；检索不保证覆盖全部相关论文。模型导读需结合原文核验。

检索窗口：arXiv &#91;2025-11-22, 2026-11-22&#41;；会议 &#91;2024-11-22, 2026-11-22&#41;（UTC，结束日不含）

## 方向概览

本导读围绕车载智能体与车企大模型这一主题，基于检索窗口内的10篇候选论文，梳理出若干相互关联的研究问题：车载助手如何在内存与延迟约束下把自然语言请求准确映射为车辆功能调用；多用户长期记忆与偏好演化如何被建模和评测；情感化与解释性交互如何服务于驾驶安全与乘客信任；以及面向自动驾驶/赛车场景的自然语言指令层如何与既有决策栈安全对接。现有工作呈现三条主线：一是函数调用与意图识别层面的轻量化部署（小型语言模型、离线语音助手、领域微调）；二是记忆、评测与仿真基础设施（可执行多用户记忆基准、车路云动态地图问答仿真）；三是人车协作与交互体验（中介式智能体、自主性分级设计、情感化回应、环境界面）。需要注意：本次候选仅10篇，且多数为预印本，缺少统一的真实车端评测标准；除个别工作外，摘要未提供可复现的代码或数据集细节，因此本导读不对未提供的经典文献、外部资源或领域事实作补充。

依据：[From Fixed Keys to Readable Schemas: Small Language Models for Vehicle Agent Function Calls](/20260822-20261119/2609.09476v2)；[VehicleMemBench: An Executable Benchmark for Multi-User Long-Term Memory in In-Vehicle Agents](/20251122-20261121/2603.23840v1)；[Vision-Language Assistant for Emotional Reactions to Risky Driving](/20251122-20261121/2607.16181v1)；[Talk to Me, Jarvis: An Open-Source Edge-Deployable Voice Assistant Framework for Autonomous Racecars](/20251122-20261121/2609.21109v1)；[MILD: Mediator Agentic System with Bidirectional Perception and Multi-Layered Alignment for Human-Vehicle Collaboration](/20251120-20261119/2605.01507v3)；[Towards Informed Autonomy Design: Understanding the Interplay of Function Characteristics and Autonomy Preferences in Automotive Agents](/20251122-20261121/2611.19474v1)；[Talk2DM: Enabling Natural Language Querying and Commonsense Reasoning for Vehicle-Road-Cloud Integrated Dynamic Maps with Large Language Models](/20251120-20261119/2602.11860v1)；[An LLM-Explainable DRL Framework for Passenger-Directed Autonomous Driving](/20251122-20261121/2606.20640v1)；[Modular Autonomy with Conversational Interaction: An LLM-driven Framework for Decision Making in Autonomous Driving](/20251122-20261121/2601.05806v1)；[When the Environment Becomes the Interface: Multisensory Environmental Interfaces for Human-AI Interaction in Autonomous Vehicles](/20251122-20261121/2609.32604v1)

## 车载功能调用与轻量化语言模型部署

该子方向关注在车端内存与延迟约束下，把自然语言请求转换为准确的车辆功能调用。相关工作报告了两类函数面表示：专用功能令牌（FT）与提示内模式（SIP），并在匹配微调条件下比较多种小型语言模型；结论指出，对训练中见过的功能，模型规模收益有限，而对留出功能只有SIP可泛化，但模式提示会带来更高推理延迟。另一项工作面向自动驾驶赛车，构建离线可部署的语音助手框架，以领域微调的7B模型作为文本到命令分类器，强调摆脱网络依赖与低延迟。还有工作把大模型作为交互层接入模块化自动驾驶栈，通过领域特定语言与安全校验层把高层指令映射到结构化动作空间。这些工作共同表明：功能面表示、领域微调与安全校验层是车端落地的关键设计点，但摘要层面的证据多来自自建基准或仿真，真实车端大规模验证仍然不足。

依据：[From Fixed Keys to Readable Schemas: Small Language Models for Vehicle Agent Function Calls](/20260822-20261119/2609.09476v2)；[Talk to Me, Jarvis: An Open-Source Edge-Deployable Voice Assistant Framework for Autonomous Racecars](/20251122-20261121/2609.21109v1)；[Modular Autonomy with Conversational Interaction: An LLM-driven Framework for Decision Making in Autonomous Driving](/20251122-20261121/2601.05806v1)

## 多用户长期记忆与可执行评测基准

随着车载智能体从简单助手转向长期陪伴，多用户偏好建模、用户间偏好冲突与习惯随时间演化成为核心问题。相关工作报告了一个基于可执行车载仿真环境的多用户长上下文记忆基准，包含多个工具模块与大量历史记忆事件，并通过比较动作后的环境状态与目标状态实现客观可复现评测，避免依赖大模型或人工打分。实验显示，强模型在直接指令任务上表现良好，但在记忆演化与偏好动态变化场景中明显吃力，现有记忆系统也难以满足领域特定需求。该方向的价值在于把记忆能力从静态问答推进到工具交互与状态可验证的评测，但候选集中仅此一篇专门基准工作，尚不足以覆盖记忆机制的多种设计路线。

依据：[VehicleMemBench: An Executable Benchmark for Multi-User Long-Term Memory in In-Vehicle Agents](/20251122-20261121/2603.23840v1)

## 人车协作、自主性设计与解释性交互

该子方向关注智能体如何与驾驶员和乘客协同，而非单向执行命令。有工作提出中介式智能体架构，联合车内与车外感知，生成合规且可解释的动作建议，并通过证据与约束加权的策略优化以及检索增强生成引入交通法规、速度建议与驾驶员偏好，实验在多个开放数据集上以可审计离线指标评估。另有工作研究不同车载功能应匹配何种自主性水平，通过专家工作坊与用户评分训练模型预测合适自主级别，并构建辅助设计工具，结论是功能特征可用于排序自主性，但面向个体用户的预测仍不确定。还有工作把深度强化学习决策与大模型解释模块结合，向乘客解释驾驶行为，并指出在请求被延迟或因安全约束被覆盖时解释最有效。这些工作共同强调透明度、约束合规与用户信任，但评测多为离线指标或小规模用户研究，跨车型泛化证据有限。

依据：[MILD: Mediator Agentic System with Bidirectional Perception and Multi-Layered Alignment for Human-Vehicle Collaboration](/20251120-20261119/2605.01507v3)；[Towards Informed Autonomy Design: Understanding the Interplay of Function Characteristics and Autonomy Preferences in Automotive Agents](/20251122-20261121/2611.19474v1)；[An LLM-Explainable DRL Framework for Passenger-Directed Autonomous Driving](/20251122-20261121/2606.20640v1)

## 情感化回应、环境界面与座舱体验

除功能与安全外，座舱智能体还被期望提供情感支持与整体体验。有工作构建视觉语言流水线，实时检测高风险驾驶行为并生成带有用户设定情感基调的语音回应，通过行车记录视频与百余名参与者的用户研究评估情感对齐，结果显示不同模型均获较好评价但偏好因用户画像而异。另一项工作提出环境界面概念，在模拟自动驾驶座舱中操纵灯光与气味，发现感知氛围对整体行程体验解释力很高，嗅觉刺激对情感反应与体验评价的影响强于视觉刺激，环境质量与感官一致性还能预测对自动驾驶系统的信任。该方向提示交互设计正从显式界面扩展到环境与多感官通道，但样本规模有限，且与语言智能体的集成方式尚未在候选中展开。

依据：[Vision-Language Assistant for Emotional Reactions to Risky Driving](/20251122-20261121/2607.16181v1)；[When the Environment Becomes the Interface: Multisensory Environmental Interfaces for Human-AI Interaction in Autonomous Vehicles](/20251122-20261121/2609.32604v1)

## 车路云协同与动态地图的自然语言查询

该子方向把车载智能体的语言能力扩展到车路云协同感知与动态地图基础设施。相关工作报告了车路云协同感知仿真框架，并构建面向混合交通场景空间查询与推理的问答数据集，进而提出即插即用的自然语言查询与常识推理模块，采用链式提示机制逐步融合人工规则与大模型常识。实验显示该模块可在不同大模型间切换并保持较高查询准确率，平均响应时间为数秒，但更大模型带来效率下降。该工作说明语言接口可成为人车路信息交互的入口，不过其评测集中在仿真问答数据上，与真实车端部署和车企大模型训练的关系在候选中证据不足。

依据：[Talk2DM: Enabling Natural Language Querying and Commonsense Reasoning for Vehicle-Road-Cloud Integrated Dynamic Maps with Large Language Models](/20251120-20261119/2602.11860v1)

## 进展与局限（基于候选证据）

综合来看，候选工作在三个层面取得进展：一是明确了车端函数调用中功能面表示与模型规模的权衡，并给出离线语音助手与安全校验交互层的可行架构；二是把记忆评测推进到多用户、可执行、状态可验证的形式；三是拓展了交互维度，包括自主性分级、解释生成、情感化回应与环境界面。局限同样明显：多数工作为预印本，评测依赖自建基准、仿真或小规模用户研究，缺少统一的真实车端指标；除个别工作声明开源外，摘要未提供可复现资源细节；关于车企自研大模型的训练数据、规模与部署经验，候选集中没有直接证据，因此本导读不对其作推断。此外，候选仅10篇，无法覆盖该领域的完整方法谱系，上述结论只反映近期检索窗口。

依据：[From Fixed Keys to Readable Schemas: Small Language Models for Vehicle Agent Function Calls](/20260822-20261119/2609.09476v2)；[VehicleMemBench: An Executable Benchmark for Multi-User Long-Term Memory in In-Vehicle Agents](/20251122-20261121/2603.23840v1)；[Talk to Me, Jarvis: An Open-Source Edge-Deployable Voice Assistant Framework for Autonomous Racecars](/20251122-20261121/2609.21109v1)；[MILD: Mediator Agentic System with Bidirectional Perception and Multi-Layered Alignment for Human-Vehicle Collaboration](/20251120-20261119/2605.01507v3)；[Towards Informed Autonomy Design: Understanding the Interplay of Function Characteristics and Autonomy Preferences in Automotive Agents](/20251122-20261121/2611.19474v1)；[Vision-Language Assistant for Emotional Reactions to Risky Driving](/20251122-20261121/2607.16181v1)；[When the Environment Becomes the Interface: Multisensory Environmental Interfaces for Human-AI Interaction in Autonomous Vehicles](/20251122-20261121/2609.32604v1)；[Talk2DM: Enabling Natural Language Querying and Commonsense Reasoning for Vehicle-Road-Cloud Integrated Dynamic Maps with Large Language Models](/20251120-20261119/2602.11860v1)

## 建议阅读顺序

以下为建议学习顺序，不是公布时间排序。

1. [From Fixed Keys to Readable Schemas: Small Language Models for Vehicle Agent Function Calls](/20260822-20261119/2609.09476v2) · 入门
   - 阅读理由：从车端最基础的功能调用问题入手，理解功能面表示与小型模型部署的权衡，是后续交互工作的技术底座。
   - 公布时间：2026-09-08（日精度）
   - arxiv · 2026-09-08（日精度）：[原文](https://arxiv.org/pdf/2609.09476v2)

2. [Talk to Me, Jarvis: An Open-Source Edge-Deployable Voice Assistant Framework for Autonomous Racecars](/20251122-20261121/2609.21109v1) · 入门
   - 阅读理由：展示离线可部署语音助手的完整链路与领域微调做法，可与上一篇的函数调用视角互补。
   - 公布时间：2026-09-17（日精度）
   - arxiv · 2026-09-17（日精度）：[原文](https://arxiv.org/pdf/2609.21109v1)

3. [Modular Autonomy with Conversational Interaction: An LLM-driven Framework for Decision Making in Autonomous Driving](/20251122-20261121/2601.05806v1) · 进阶
   - 阅读理由：把语言交互层接入模块化自动驾驶栈，理解领域特定语言与安全校验层的作用。
   - 公布时间：2026-01-09（日精度）
   - arxiv · 2026-01-09（日精度）：[原文](https://arxiv.org/pdf/2601.05806v1)

4. [VehicleMemBench: An Executable Benchmark for Multi-User Long-Term Memory in In-Vehicle Agents](/20251122-20261121/2603.23840v1) · 进阶
   - 阅读理由：转向长期记忆与多用户偏好，了解可执行、状态可验证的评测设计。
   - 公布时间：2026-03-25（日精度）
   - arxiv · 2026-03-25（日精度）：[原文](https://arxiv.org/pdf/2603.23840v1)

5. [MILD: Mediator Agentic System with Bidirectional Perception and Multi-Layered Alignment for Human-Vehicle Collaboration](/20251120-20261119/2605.01507v3) · 进阶
   - 阅读理由：从单向指令扩展到人车双向协作与可解释策略，连接功能层与协作层。
   - 公布时间：2026-05-02（日精度）
   - arxiv · 2026-05-02（日精度）：[原文](https://arxiv.org/pdf/2605.01507v3)

6. [Towards Informed Autonomy Design: Understanding the Interplay of Function Characteristics and Autonomy Preferences in Automotive Agents](/20251122-20261121/2611.19474v1) · 进阶
   - 阅读理由：理解不同功能应匹配的自主性水平及设计辅助方法，补充交互设计视角。
   - 公布时间：2026-11-14（日精度）
   - arxiv · 2026-11-14（日精度）：[原文](https://arxiv.org/pdf/2611.19474v1)

7. [An LLM-Explainable DRL Framework for Passenger-Directed Autonomous Driving](/20251122-20261121/2606.20640v1) · 进阶
   - 阅读理由：了解强化学习决策与大模型解释模块的结合方式及解释触发时机。
   - 公布时间：2026-06-02（日精度）
   - arxiv · 2026-06-02（日精度）：[原文](https://arxiv.org/pdf/2606.20640v1)

8. [Vision-Language Assistant for Emotional Reactions to Risky Driving](/20251122-20261121/2607.16181v1) · 专题
   - 阅读理由：进入情感化回应与用户偏好维度，观察多模型情感对齐的评估方式。
   - 公布时间：2026-07-17（日精度）
   - arxiv · 2026-07-17（日精度）：[原文](https://arxiv.org/pdf/2607.16181v1)

9. [When the Environment Becomes the Interface: Multisensory Environmental Interfaces for Human-AI Interaction in Autonomous Vehicles](/20251122-20261121/2609.32604v1) · 专题
   - 阅读理由：从显式界面扩展到多感官环境界面，理解座舱体验与信任的非语言通道。
   - 公布时间：2026-09-26（日精度）
   - arxiv · 2026-09-26（日精度）：[原文](https://arxiv.org/pdf/2609.32604v1)

10. [Talk2DM: Enabling Natural Language Querying and Commonsense Reasoning for Vehicle-Road-Cloud Integrated Dynamic Maps with Large Language Models](/20251120-20261119/2602.11860v1) · 专题
   - 阅读理由：最后看车路云协同与动态地图的自然语言查询，把视野从单车扩展到基础设施侧。
   - 公布时间：2026-02-12（日精度）
   - arxiv · 2026-02-12（日精度）：[原文](https://arxiv.org/pdf/2602.11860v1)

任务：研究方向大礼包

固定窗口：arXiv &#91;2025-11-22, 2026-11-22&#41;；会议 &#91;2024-11-22, 2026-11-22&#41;（UTC，结束日不含）

本次候选评审上限 300，最终名单上限 100；本轮内容预算 10。

覆盖限制：仅检索配置范围内已有库存与预算内候选；向量/会议Top-k召回并非全库遍历，不保证找全相关论文。未核实录用、日期边界和缺失库存不能当作已覆盖。

缺失库存：eccv 2025、emnlp 2026、neurips 2026。

研究需求：车载智能体，车企大模型

# car-ai-agent

以下为本次固定最终名单，按相关性评分降序；不代表全部相关论文。

1. [From Fixed Keys to Readable Schemas: Small Language Models for Vehicle Agent Function Calls](https://arxiv.org/abs/2609.09476v2) · 分数 9
2. [VehicleMemBench: An Executable Benchmark for Multi-User Long-Term Memory in In-Vehicle Agents](https://arxiv.org/abs/2603.23840v1) · 分数 9
3. [Vision-Language Assistant for Emotional Reactions to Risky Driving](https://arxiv.org/abs/2607.16181v1) · 分数 8
4. [Talk to Me, Jarvis: An Open-Source Edge-Deployable Voice Assistant Framework for Autonomous Racecars](https://arxiv.org/abs/2609.21109v1) · 分数 7
5. [MILD: Mediator Agentic System with Bidirectional Perception and Multi-Layered Alignment for Human-Vehicle Collaboration](https://arxiv.org/abs/2605.01507v3) · 分数 7
6. [Towards Informed Autonomy Design: Understanding the Interplay of Function Characteristics and Autonomy Preferences in Automotive Agents](https://arxiv.org/abs/2611.19474v1) · 分数 7
7. [Talk2DM: Enabling Natural Language Querying and Commonsense Reasoning for Vehicle-Road-Cloud Integrated Dynamic Maps with Large Language Models](https://arxiv.org/abs/2602.11860v1) · 分数 6
8. [An LLM-Explainable DRL Framework for Passenger-Directed Autonomous Driving](https://arxiv.org/abs/2606.20640v1) · 分数 6
9. [Modular Autonomy with Conversational Interaction: An LLM-driven Framework for Decision Making in Autonomous Driving](https://arxiv.org/abs/2601.05806v1) · 分数 6
10. [When the Environment Becomes the Interface: Multisensory Environmental Interfaces for Human-AI Interaction in Autonomous Vehicles](https://arxiv.org/abs/2609.32604v1) · 分数 6

[按公布时间查看](#/starter-pack/20261122-f7bf6220a719/dates)

阅读内容：已完成 10，待补充 0。
