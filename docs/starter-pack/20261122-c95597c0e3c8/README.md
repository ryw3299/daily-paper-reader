<div class="dpr-topic-result-actions"><button type="button" data-topic-copy="docs/starter-pack/20261122-c95597c0e3c8/papers.md">复制论文清单</button> <a href="docs/starter-pack/20261122-c95597c0e3c8/papers.md" download data-no-router>下载 Markdown</a> <a href="docs/starter-pack/20261122-c95597c0e3c8/papers.json" download data-no-router>下载 JSON</a> <button type="button" data-topic-continue="20261122-c95597c0e3c8">继续生成阅读内容</button></div>

# car-ai-agent · 入门导读

> 本导读基于所列论文的标题、摘要和已有速览，不代表已阅读全部全文。近期窗口不是完整领域史；检索不保证覆盖全部相关论文。模型导读需结合原文核验。

检索窗口：arXiv &#91;2025-11-22, 2026-11-22&#41;；会议 &#91;2024-11-22, 2026-11-22&#41;（UTC，结束日不含）

## 方向概览

本导读聚焦车载智能体与车企大模型这一近期检索窗口内的研究问题：如何在车内座舱与服务场景中，把自然语言请求转化为可靠的车辆功能调用、状态查询与行为决策，并在多用户、长时记忆、情感与安全约束、端侧算力限制下保持可用性。输入论文显示三条主要线索：一是以函数调用与指令实现为核心的交互层设计，关注小模型端侧部署、函数表面表示、DSL 与安全校验、多规划器调度；二是面向长期陪伴的记忆与多用户偏好建模，强调可执行仿真与客观评测；三是面向驾驶与物理世界的多模态基础模型与情感化、主动式交互设计。评测方面，已有工作多采用自建基准、仿真闭环、环境状态比对或用户研究，但各基准之间尚不统一。局限包括：多数系统在真实道路与量产车机上的验证有限，长时记忆与偏好演化仍是薄弱环节，端侧模型在未见函数上的泛化与拒答能力不足，情感与自主性设计对个体用户的预测仍不确定。本导读只覆盖给定候选论文，不构成该领域完整历史。

依据：[From Fixed Keys to Readable Schemas: Small Language Models for Vehicle Agent Function Calls](/20260822-20261119/2609.09476v2)；[VehicleMemBench: An Executable Benchmark for Multi-User Long-Term Memory in In-Vehicle Agents](/20251122-20261121/2603.23840v1)；[Modular Autonomy with Conversational Interaction: An LLM-driven Framework for Decision Making in Autonomous Driving](/20251122-20261121/2601.05806v1)；[Talk to Me, Jarvis: An Open-Source Edge-Deployable Voice Assistant Framework for Autonomous Racecars](/20251122-20261121/2609.21109v1)；[Vision-Language Assistant for Emotional Reactions to Risky Driving](/20251122-20261121/2607.16181v1)；[MILD: Mediator Agentic System with Bidirectional Perception and Multi-Layered Alignment for Human-Vehicle Collaboration](/20251120-20261119/2605.01507v3)；[Towards Informed Autonomy Design: Understanding the Interplay of Function Characteristics and Autonomy Preferences in Automotive Agents](/20251122-20261121/2611.19474v1)；[Talk2DM: Enabling Natural Language Querying and Commonsense Reasoning for Vehicle-Road-Cloud Integrated Dynamic Maps with Large Language Models](/20251120-20261119/2602.11860v1)；[TuringPAI: A Foundation for On-Device Physical AI](/20251120-20261119/2611.25474v1)；[Open-Ended Instruction Realization with LLM-Enabled Multi-Planner Scheduling in Autonomous Vehicles](/20251122-20261121/2604.08031v1)

## 车辆功能调用与自然语言指令落地

该子方向关注如何把驾驶者或乘客的自然语言请求映射为车辆可执行的功能调用或控制信号。arxiv:2609.09476 比较功能令牌与提示内模式两种函数表面表示，指出表示方式而非单纯模型规模决定小模型在已见函数、未见函数与越界请求上的能力与失败模式。arxiv:2601.05806 在模块化自动驾驶栈上引入大模型交互层，通过交互分类、领域特定语言与安全校验层把高层命令翻译为结构化动作。arxiv:2604.08031 以脚本调度多个模型预测控制规划器，将语义推理与车辆控制解耦，并构建闭环基准评估开放式指令实现。arxiv:2602.11860 面向车路云动态地图，用链式提示机制支持自然语言空间查询与常识推理。这些工作共同显示：函数或动作空间的表示、校验与调度是落地关键，但各系统接口与评测环境差异较大，跨系统可比性有限。

依据：[From Fixed Keys to Readable Schemas: Small Language Models for Vehicle Agent Function Calls](/20260822-20261119/2609.09476v2)；[Modular Autonomy with Conversational Interaction: An LLM-driven Framework for Decision Making in Autonomous Driving](/20251122-20261121/2601.05806v1)；[Open-Ended Instruction Realization with LLM-Enabled Multi-Planner Scheduling in Autonomous Vehicles](/20251122-20261121/2604.08031v1)；[Talk2DM: Enabling Natural Language Querying and Commonsense Reasoning for Vehicle-Road-Cloud Integrated Dynamic Maps with Large Language Models](/20251120-20261119/2602.11860v1)

## 端侧部署与低延迟语音交互

车载场景对内存、延迟与网络依赖敏感，端侧小模型与离线语音框架是重要路线。arxiv:2609.09476 在 270M 至 1.7B 参数的小模型上比较函数表面表示，强调端侧部署约束下的设计取舍。arxiv:2609.21109 提出面向自动驾驶赛车的离线语音助手框架，用领域微调的 Mistral 7B 做文本到命令分类，报告了意图识别准确率与平均处理延迟，并开源实现。arxiv:2611.25474 展示面向端侧物理 AI 的模型家族，其中驾驶模型在单颗 Orin-X 上以 12Hz 生成轨迹。这些结果说明端侧可行，但输入论文未提供量产车机长期运行或跨车型泛化的证据，相关结论应限于所述实验条件。

依据：[From Fixed Keys to Readable Schemas: Small Language Models for Vehicle Agent Function Calls](/20260822-20261119/2609.09476v2)；[Talk to Me, Jarvis: An Open-Source Edge-Deployable Voice Assistant Framework for Autonomous Racecars](/20251122-20261121/2609.21109v1)；[TuringPAI: A Foundation for On-Device Physical AI](/20251120-20261119/2611.25474v1)

## 多用户长时记忆与个性化服务

从简单助手走向长期陪伴，需要持续建模多用户偏好并处理偏好冲突与演化。arxiv:2603.23840 提出基于可执行车内仿真环境的多用户长上下文记忆基准，包含 23 个工具模块与每条样本 80 余条历史记忆事件，通过比较动作后环境状态与目标状态实现客观可复现评测，无需大模型或人工打分。其实验显示强模型在直接指令任务上表现良好，但在记忆演化与偏好动态变化场景中明显吃力，现有记忆系统也难以满足领域特定需求。该方向目前主要证据来自仿真基准，真实车内长期部署数据在输入中未见。

依据：[VehicleMemBench: An Executable Benchmark for Multi-User Long-Term Memory in In-Vehicle Agents](/20251122-20261121/2603.23840v1)

## 多模态感知、情感交互与人车协同

部分工作把智能体从命令执行扩展到情感表达与人车协同。arxiv:2607.16181 用视觉模块检测危险驾驶行为并生成结构化行为日志，再由大模型按用户设定的情感语气生成口头反应，用户研究涉及 108 名参与者，报告了不同模型组合的评分。arxiv:2605.01507 提出中介者代理系统，联合舱内与舱外感知，用证据与约束加权策略优化和检索增强生成把交通法规、速度建议与驾驶者偏好纳入决策，实验覆盖三个开放数据集并包含人工评分。arxiv:2611.19474 通过专家工作坊与 126 名参与者对 14 项车内功能的自主性偏好评分，训练模型预测合适自主级别，并开发自主性设计助手原型；结果显示功能特征可用于排序自主级别，但个体用户预测仍不确定。这些研究提示情感与自主性设计需与安全约束共同考虑，但样本规模与场景仍有限。

依据：[Vision-Language Assistant for Emotional Reactions to Risky Driving](/20251122-20261121/2607.16181v1)；[MILD: Mediator Agentic System with Bidirectional Perception and Multi-Layered Alignment for Human-Vehicle Collaboration](/20251120-20261119/2605.01507v3)；[Towards Informed Autonomy Design: Understanding the Interplay of Function Characteristics and Autonomy Preferences in Automotive Agents](/20251122-20261121/2611.19474v1)

## 评测方式、进展与局限

输入论文的评测方式可分为四类：自建函数调用基准与留出函数测试（arxiv:2609.09476）；可执行仿真环境中的状态比对（arxiv:2603.23840）；闭环仿真与任务完成率、查询成本、安全合规指标（arxiv:2604.08031）；用户研究与人工评分（arxiv:2607.16181、arxiv:2605.01507、arxiv:2611.19474）。进展在于评测从静态问答转向可执行、可复现和多用户长时场景，并开始纳入拒答、安全校验与延迟等部署指标。局限在于：基准规模与函数覆盖面有限，仿真与真实道路之间存在差距，长时记忆与偏好演化缺乏真实部署验证，端侧小模型在未见函数上的泛化依赖提示内模式并带来延迟代价，情感与自主性设计对个体用户的预测尚不确定。输入未提供统一排行榜或跨论文复现结果，因此不宜据此比较系统绝对优劣。

依据：[From Fixed Keys to Readable Schemas: Small Language Models for Vehicle Agent Function Calls](/20260822-20261119/2609.09476v2)；[VehicleMemBench: An Executable Benchmark for Multi-User Long-Term Memory in In-Vehicle Agents](/20251122-20261121/2603.23840v1)；[Open-Ended Instruction Realization with LLM-Enabled Multi-Planner Scheduling in Autonomous Vehicles](/20251122-20261121/2604.08031v1)；[Vision-Language Assistant for Emotional Reactions to Risky Driving](/20251122-20261121/2607.16181v1)；[MILD: Mediator Agentic System with Bidirectional Perception and Multi-Layered Alignment for Human-Vehicle Collaboration](/20251120-20261119/2605.01507v3)；[Towards Informed Autonomy Design: Understanding the Interplay of Function Characteristics and Autonomy Preferences in Automotive Agents](/20251122-20261121/2611.19474v1)

## 建议阅读顺序

以下为建议学习顺序，不是公布时间排序。

1. [From Fixed Keys to Readable Schemas: Small Language Models for Vehicle Agent Function Calls](/20260822-20261119/2609.09476v2) · 入门
   - 阅读理由：从车辆功能调用这一核心问题入手，理解函数表面表示对小模型能力与失败模式的影响，是后续端侧与评测讨论的基础。
   - 公布时间：2026-09-08（日精度）
   - arxiv · 2026-09-08（日精度）：[原文](https://arxiv.org/pdf/2609.09476v2)

2. [Modular Autonomy with Conversational Interaction: An LLM-driven Framework for Decision Making in Autonomous Driving](/20251122-20261121/2601.05806v1) · 入门
   - 阅读理由：展示大模型交互层如何通过分类、领域特定语言与安全校验接入模块化自动驾驶栈，建立指令到动作的完整链路认识。
   - 公布时间：2026-01-09（日精度）
   - arxiv · 2026-01-09（日精度）：[原文](https://arxiv.org/pdf/2601.05806v1)

3. [Talk to Me, Jarvis: An Open-Source Edge-Deployable Voice Assistant Framework for Autonomous Racecars](/20251122-20261121/2609.21109v1) · 入门
   - 阅读理由：提供离线端侧语音助手的完整框架与延迟、准确率证据，适合理解端侧部署取舍。
   - 公布时间：2026-09-17（日精度）
   - arxiv · 2026-09-17（日精度）：[原文](https://arxiv.org/pdf/2609.21109v1)

4. [VehicleMemBench: An Executable Benchmark for Multi-User Long-Term Memory in In-Vehicle Agents](/20251122-20261121/2603.23840v1) · 进阶
   - 阅读理由：转向多用户长时记忆问题，理解可执行仿真基准如何客观评测记忆与工具使用。
   - 公布时间：2026-03-25（日精度）
   - arxiv · 2026-03-25（日精度）：[原文](https://arxiv.org/pdf/2603.23840v1)

5. [Open-Ended Instruction Realization with LLM-Enabled Multi-Planner Scheduling in Autonomous Vehicles](/20251122-20261121/2604.08031v1) · 进阶
   - 阅读理由：学习开放式指令如何通过多规划器调度落地，并关注闭环基准与延迟容忍设计。
   - 公布时间：2026-04-09（日精度）
   - arxiv · 2026-04-09（日精度）：[原文](https://arxiv.org/pdf/2604.08031v1)

6. [Talk2DM: Enabling Natural Language Querying and Commonsense Reasoning for Vehicle-Road-Cloud Integrated Dynamic Maps with Large Language Models](/20251120-20261119/2602.11860v1) · 进阶
   - 阅读理由：扩展至车路云动态地图的自然语言查询与常识推理，理解链式提示与跨模型切换。
   - 公布时间：2026-02-12（日精度）
   - arxiv · 2026-02-12（日精度）：[原文](https://arxiv.org/pdf/2602.11860v1)

7. [TuringPAI: A Foundation for On-Device Physical AI](/20251120-20261119/2611.25474v1) · 进阶
   - 阅读理由：了解端侧物理 AI 基础模型家族及其在驾驶与机器人操作上的统一视觉语言初始化。
   - 公布时间：2026-11-19（日精度）
   - arxiv · 2026-11-19（日精度）：[原文](https://arxiv.org/pdf/2611.25474v1)

8. [Vision-Language Assistant for Emotional Reactions to Risky Driving](/20251122-20261121/2607.16181v1) · 专题
   - 阅读理由：进入情感化交互方向，理解风险检测与情感语气生成结合的管线及用户研究设计。
   - 公布时间：2026-07-17（日精度）
   - arxiv · 2026-07-17（日精度）：[原文](https://arxiv.org/pdf/2607.16181v1)

9. [MILD: Mediator Agentic System with Bidirectional Perception and Multi-Layered Alignment for Human-Vehicle Collaboration](/20251120-20261119/2605.01507v3) · 专题
   - 阅读理由：深入人车协同的中介者架构，关注双向感知、约束对齐与可解释策略生成。
   - 公布时间：2026-05-02（日精度）
   - arxiv · 2026-05-02（日精度）：[原文](https://arxiv.org/pdf/2605.01507v3)

10. [Towards Informed Autonomy Design: Understanding the Interplay of Function Characteristics and Autonomy Preferences in Automotive Agents](/20251122-20261121/2611.19474v1) · 专题
   - 阅读理由：从设计角度理解功能特征与自主性级别的关系，以及个体用户预测的不确定性。
   - 公布时间：2026-11-14（日精度）
   - arxiv · 2026-11-14（日精度）：[原文](https://arxiv.org/pdf/2611.19474v1)

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
3. [Modular Autonomy with Conversational Interaction: An LLM-driven Framework for Decision Making in Autonomous Driving](https://arxiv.org/abs/2601.05806v1) · 分数 8
4. [Talk to Me, Jarvis: An Open-Source Edge-Deployable Voice Assistant Framework for Autonomous Racecars](https://arxiv.org/abs/2609.21109v1) · 分数 7
5. [Vision-Language Assistant for Emotional Reactions to Risky Driving](https://arxiv.org/abs/2607.16181v1) · 分数 7
6. [MILD: Mediator Agentic System with Bidirectional Perception and Multi-Layered Alignment for Human-Vehicle Collaboration](https://arxiv.org/abs/2605.01507v3) · 分数 7
7. [Towards Informed Autonomy Design: Understanding the Interplay of Function Characteristics and Autonomy Preferences in Automotive Agents](https://arxiv.org/abs/2611.19474v1) · 分数 7
8. [Talk2DM: Enabling Natural Language Querying and Commonsense Reasoning for Vehicle-Road-Cloud Integrated Dynamic Maps with Large Language Models](https://arxiv.org/abs/2602.11860v1) · 分数 6
9. [TuringPAI: A Foundation for On-Device Physical AI](https://arxiv.org/abs/2611.25474v1) · 分数 6
10. [Open-Ended Instruction Realization with LLM-Enabled Multi-Planner Scheduling in Autonomous Vehicles](https://arxiv.org/abs/2604.08031v1) · 分数 6

[按公布时间查看](#/starter-pack/20261122-c95597c0e3c8/dates)

阅读内容：已完成 10，待补充 0。
