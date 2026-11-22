<div class="dpr-topic-result-actions"><button type="button" data-topic-copy="docs/starter-pack/20261122-a04aee8c6135/papers.md">复制论文清单</button> <a href="docs/starter-pack/20261122-a04aee8c6135/papers.md" download data-no-router>下载 Markdown</a> <a href="docs/starter-pack/20261122-a04aee8c6135/papers.json" download data-no-router>下载 JSON</a> <button type="button" data-topic-continue="20261122-a04aee8c6135">继续生成阅读内容</button></div>

# in-car-agent · 入门导读

> 本导读基于所列论文的标题、摘要和已有速览，不代表已阅读全部全文。近期窗口不是完整领域史；检索不保证覆盖全部相关论文。模型导读需结合原文核验。

检索窗口：arXiv &#91;2025-11-22, 2026-11-22&#41;；会议 &#91;2024-11-22, 2026-11-22&#41;（UTC，结束日不含）

## 方向概览

本导读围绕车载智能体（in-car-agent）如何理解驾驶员或乘客需求、结合情境决定追问/提醒/执行，并覆盖任务型对话、主动交互、导航出行、工具调用与车辆功能操作。近期工作大致分为几条主线：一是面向车辆功能调用的轻量模型与函数表面表示（如功能令牌与提示内模式），关注小模型在内存与延迟约束下的泛化与拒答；二是面向乘客语言指令的驾驶行为条件化与规划，涵盖多阶段意图数据集、指令条件化轨迹生成、开放指令到多规划器调度、语言驱动代价优化以及语言世界模型的安全前瞻；三是记忆与个性化，包括多用户长期记忆的可执行基准和个性化公交路线规划；四是主动交互与自主性设计，研究功能特性与合适自主等级的映射；五是情感与多模态交互，包括风险驾驶的情绪化反馈、语音情感线索与VLA结合、座舱环境作为界面；六是评测与安全，包括反事实指令跟随基准、导航冲突感知与对抗鲁棒性、以及停车失效与人类交互安全分析。整体上，证据显示语言接口正在从固定命令集扩展到自由指令，但语言控制可靠性与长时意图保持仍是明显短板；多个基准与数据集为可复现评测提供了基础，但多数系统仍在仿真或离线指标下验证，真实道路与多用户长期部署证据有限。

依据：[From Fixed Keys to Readable Schemas: Small Language Models for Vehicle Agent Function Calls](/20260822-20261119/2609.09476v2)；[VehicleMemBench: An Executable Benchmark for Multi-User Long-Term Memory in In-Vehicle Agents](/20251122-20261121/2603.23840v1)；[Talk to Me, Jarvis: An Open-Source Edge-Deployable Voice Assistant Framework for Autonomous Racecars](/20251122-20261121/2609.21109v1)；[Towards Informed Autonomy Design: Understanding the Interplay of Function Characteristics and Autonomy Preferences in Automotive Agents](/20251122-20261121/2611.19474v1)；[MILD: Mediator Agentic System with Bidirectional Perception and Multi-Layered Alignment for Human-Vehicle Collaboration](/20251120-20261119/2605.01507v3)；[Vision-Language Assistant for Emotional Reactions to Risky Driving](/20251122-20261121/2607.16181v1)；[Modular Autonomy with Conversational Interaction: An LLM-driven Framework for Decision Making in Autonomous Driving](/20251122-20261121/2601.05806v1)；[An LLM-Explainable DRL Framework for Passenger-Directed Autonomous Driving](/20251122-20261121/2606.20640v1)；[doPlan: A Variable-Horizon Dataset for Multi-Stage Language-Conditioned Planning in Autonomous Driving](/20251122-20261121/2609.38028v1)；[Listen, Look, Drive: Coupling Audio Instructions for User-aware VLA-based Autonomous Driving](/20251122-20261121/2601.12142v3)；[A Large-Language-Model Supported Personalized Driving Framework for Lane Change in Highway Scenarios](/20251120-20261119/2606.31483v2)；[Language2Drive: Do Vision-Language-Action Models Really Follow the Instructions in Autonomous Driving?](/20251122-20261121/2610.16634v1)；[When the Environment Becomes the Interface: Multisensory Environmental Interfaces for Human-AI Interaction in Autonomous Vehicles](/20251122-20261121/2609.32604v1)；[Jev with Foresight: Safe Language-Guided Autonomous Driving via a Language World Model](/20260822-20261119/2611.05448v1)；[Talk2DM: Enabling Natural Language Querying and Commonsense Reasoning for Vehicle-Road-Cloud Integrated Dynamic Maps with Large Language Models](/20251120-20261119/2602.11860v1)；[Natural Language Instructions for Scene-Responsive Human-in-the-Loop Motion Planning in Autonomous Driving using Vision-Language-Action Models](/20251122-20261121/2602.04184v1)；[Open-Ended Instruction Realization with LLM-Enabled Multi-Planner Scheduling in Autonomous Vehicles](/20251122-20261121/2604.08031v1)；[From Human Intention to Action Prediction: Intention-Driven End-to-End Autonomous Driving](/20251122-20261121/2512.12302v2)；[Language-Driven Cost Optimization for Autonomous Driving](/20251122-20261121/2606.10974v1)；[SafeDriveVLA: Navigation-Conditioned World Model Dreaming for Conflict-Aware End-to-End Autonomous Driving](/20260822-20261119/2610.20609v1)；[When Stopping Fails: Rethinking Minimal Risk Conditions through Human-Interactive Autonomous Driving for Safe Transportation Systems](/20251122-20261121/2606.29115v1)；[E3AD: An Emotion-Aware Vision-Language-Action Model for Human-Centric End-to-End Autonomous Driving](/20251122-20261121/2512.04733v3)；[ChatPlanner: A Large Language Model Framework for Personalized Public Transit Routing](/20251122-20261121/2606.15315v3)

## 车辆功能调用与车载对话接口

该子方向关注把自然语言请求映射为车辆功能调用或高层行为命令，并在资源受限的车载环境中保持可用性。一篇工作比较功能令牌与提示内模式两种函数表面表示，在9822条单轮样例、79个车辆功能上比较四个小模型，发现训练中见过的功能上规模收益有限，而未见功能上只有提示内模式能泛化，但模式提示带来更高推理延迟；超出范围请求时功能令牌可能调用不可用功能。另一篇工作构建面向自动驾驶赛车的高层行为命令离线语音助手，用领域微调的Mistral 7B做文本到命令分类，报告97.63%意图识别准确率与平均1.39秒处理延迟，并提供开源实现。还有工作把LLM交互层与Autoware模块化栈结合，通过交互分类、应用级DSL和安全性校验层，让乘客查询状态或修改驾驶行为，并在仿真中验证五类交互。这些工作共同表明：函数/命令的表面表示和校验层设计对能力边界与失败模式有实质影响，但证据多来自单轮或仿真设定，多轮追问与澄清的覆盖仍有限。

依据：[From Fixed Keys to Readable Schemas: Small Language Models for Vehicle Agent Function Calls](/20260822-20261119/2609.09476v2)；[Talk to Me, Jarvis: An Open-Source Edge-Deployable Voice Assistant Framework for Autonomous Racecars](/20251122-20261121/2609.21109v1)；[Modular Autonomy with Conversational Interaction: An LLM-driven Framework for Decision Making in Autonomous Driving](/20251122-20261121/2601.05806v1)

## 乘客语言指令驱动的驾驶规划与行为条件化

这一组工作研究如何把乘客的自由语言意图转化为可执行的驾驶行为或规划参数。doPlan构建基于nuPlan的真实乘客指令数据集，包含5154条指令、覆盖即时、延迟、事件条件、持续和多阶段意图，并指出在2161个有匹配未来机动的样例中，首个相关机动中位出现在评估点后24.6秒，仅9.8%落在常见5秒预测窗口内，说明长时意图与规划衔接仍是缺口。doScenes相关工作把自由指令接入OpenEMMA端到端框架，在849个场景上报告指令条件化大幅减少极端失败，剔除离群后良好措辞的提示可提升ADE最多5.1%。另有工作提出开放指令实现框架，用LLM生成脚本调度多个MPC规划器，并在闭环基准中报告任务完成率提升、查询成本降低和对推理延迟的容忍。语言驱动代价优化工作让LLM根据场景描述与用户查询生成MPPI控制器参数，并加入人在回路确认。个性化车道变换工作把自然语言偏好映射为Apollo规划参数，并用RAG解释隐式命令。Jev-AD则用类型化决策模型加语言世界模型预测候选动作后果，在仿真合流与NGSIM回放中报告碰撞率下降。总体看，指令条件化能改善行为对齐，但反事实指令跟随与长时意图保持仍是薄弱环节。

依据：[doPlan: A Variable-Horizon Dataset for Multi-Stage Language-Conditioned Planning in Autonomous Driving](/20251122-20261121/2609.38028v1)；[Natural Language Instructions for Scene-Responsive Human-in-the-Loop Motion Planning in Autonomous Driving using Vision-Language-Action Models](/20251122-20261121/2602.04184v1)；[Open-Ended Instruction Realization with LLM-Enabled Multi-Planner Scheduling in Autonomous Vehicles](/20251122-20261121/2604.08031v1)；[Language-Driven Cost Optimization for Autonomous Driving](/20251122-20261121/2606.10974v1)；[A Large-Language-Model Supported Personalized Driving Framework for Lane Change in Highway Scenarios](/20251120-20261119/2606.31483v2)；[Jev with Foresight: Safe Language-Guided Autonomous Driving via a Language World Model](/20260822-20261119/2611.05448v1)

## 多阶段意图、反事实评测与语言控制可靠性

评测工作开始区分“驾驶成功”与“语言被遵循”。Language2Drive提出配对反事实单元，在固定初始场景下只改变指令，并在CARLA闭环、重建真实场景和开环基准中评测代表性驾驶VLA，报告93.2%的成功 rollout 在替代可行指令下没有成功对应，失败以单侧完成为主，说明常规驾驶分数会高估语言跟随能力。Intention-Drive把意图驱动端到端驾驶形式化为任务，构建大规模自然语言意图与高保真传感器数据配对的基准，并提出 Imagined Future Alignment 评价协议，实验显示现有模型驾驶稳定性尚可但意图满足明显不足。SafeDriveVLA则同时评测导航跟随、冲突感知与对抗鲁棒性，报告现有VLA在冲突信号下显著退化，并提出三级导航遵从模式与导航条件世界模型 dreaming，在Bench2Drive上报告88.16驾驶分数与68.64%成功率，并将不安全指令下碰撞从60降到38。这些证据表明语言接口的开放化暴露了新的安全面，评测需要成对反事实与冲突条件，而不仅是路线完成与安全性。

依据：[Language2Drive: Do Vision-Language-Action Models Really Follow the Instructions in Autonomous Driving?](/20251122-20261121/2610.16634v1)；[From Human Intention to Action Prediction: Intention-Driven End-to-End Autonomous Driving](/20251122-20261121/2512.12302v2)；[SafeDriveVLA: Navigation-Conditioned World Model Dreaming for Conflict-Aware End-to-End Autonomous Driving](/20260822-20261119/2610.20609v1)

## 长期记忆、多用户偏好与个性化服务

车载智能体要从单次助手走向长期伴侣，需要建模多用户偏好及其随时间变化。VehicleMemBench构建在可执行车载仿真环境上的多用户长上下文记忆基准，包含23个工具模块，每个样本含80余条历史记忆事件，通过比较动作后环境状态与目标状态做客观可复现评测，不依赖LLM或人工打分；实验显示强模型在直接指令任务上表现良好，但在记忆演化、尤其用户偏好动态变化时明显吃力，现有记忆系统也难以处理领域特定记忆需求。ChatPlanner面向个性化公共交通路线，用微调LLM加RAG从对话中抽取路线参数与偏好分数并融入目标函数，在八种人物设定与五种情境的数据上验证可行性、抽取准确性与延迟可计算性。两者分别覆盖车内多用户长期记忆与出行服务个性化，但前者为仿真基准，后者为公交路线规划，尚不能直接等同于真实车内多用户部署证据。

依据：[VehicleMemBench: An Executable Benchmark for Multi-User Long-Term Memory in In-Vehicle Agents](/20251122-20261121/2603.23840v1)；[ChatPlanner: A Large Language Model Framework for Personalized Public Transit Routing](/20251122-20261121/2606.15315v3)

## 主动交互、自主性等级与人车协同

主动交互的核心问题是系统应在何时追问、提醒或自主执行。一项工作通过专家工作坊定义自主等级与功能特性，收集126名参与者对14项车内功能的自主偏好与功能特性评分，训练模型预测合适自主等级，并开发自主设计助手供设计者使用；结果显示功能特性可用于排序合适自主等级，但面向个体用户的预测仍不确定。MILD提出中介者在环的智能体架构，联合车内外感知与轻量策略智能体生成可解释动作建议，并用证据与约束加权策略优化和检索增强生成引入交通法规、速度建议与驾驶员偏好，在三个开放数据集上报告感知与策略质量优于基线，并获得更高的人工评分政策适当性、舒适性与解释性。这些工作把“是否执行”从固定规则推向基于功能特性与约束的设计，但个体化自主决策的可靠性证据仍有限。

依据：[Towards Informed Autonomy Design: Understanding the Interplay of Function Characteristics and Autonomy Preferences in Automotive Agents](/20251122-20261121/2611.19474v1)；[MILD: Mediator Agentic System with Bidirectional Perception and Multi-Layered Alignment for Human-Vehicle Collaboration](/20251120-20261119/2605.01507v3)

## 情感、语音与多模态座舱交互

多模态与情感线索被用于让车载交互更贴近乘客状态。KYA用YOLOv8变体检测风险驾驶行为并生成结构化行为日志，再由LLM按用户设定的情绪语气生成口头反应，108名参与者的用户研究显示所有模型获正面评价但偏好因人物设定而异，YOLOv8s与ChatGPT-4o组合得分最高4.29/5。EchoVLA把相机流与现场音频指令耦合，用合成语音与情感语音-轨迹对构建多模态思维链微调Qwen2.5-Omni，在开环基准上报告平均L2误差降低59.4%、碰撞率降低74.4%，并显示语音情感可调制驾驶行为。E3AD引入连续Valence-Arousal-Dominance情感模型与双路径空间推理，在真实数据集上报告视觉 grounding、路点规划与情感估计VAD相关性达到SOTA。另有工作把座舱环境本身视为界面，24名参与者、216次观测的实验显示感知氛围解释整体旅程体验66.5%的方差，嗅觉刺激对情感与体验评价影响强于视觉，环境质量与感官一致性预测对自动驾驶系统的信任。这些证据支持情感与多模态通道的价值，但样本规模与仿真设定限制了外推。

依据：[Vision-Language Assistant for Emotional Reactions to Risky Driving](/20251122-20261121/2607.16181v1)；[Listen, Look, Drive: Coupling Audio Instructions for User-aware VLA-based Autonomous Driving](/20251122-20261121/2601.12142v3)；[E3AD: An Emotion-Aware Vision-Language-Action Model for Human-Centric End-to-End Autonomous Driving](/20251122-20261121/2512.04733v3)；[When the Environment Becomes the Interface: Multisensory Environmental Interfaces for Human-AI Interaction in Autonomous Vehicles](/20251122-20261121/2609.32604v1)

## 导航、车路云信息查询与安全交互边界

导航与出行信息服务方面，Talk2DM面向车路云一体化动态地图，构建VRCsim仿真框架与VRC-QA问答数据集，提出基于链式提示的即插即用模块，实验报告在Qwen3:8B、Gemma3:27B与GPT-oss等模型上超过93%的自然语言查询准确率、平均响应2至5秒，并指出更大模型准确率更高但效率下降。安全交互边界方面，一项分析基于公开记录的自动驾驶停车行为与人车交互失败事件，按感知、规划与控制局限分类，指出仅靠减速或停车的最小风险条件不足以应对交通阻塞、应急响应与可达性问题，并讨论人类权威解释、多模态指令响应、语言 grounding 与远程协助等方向。该分析强调从被动回退走向人类交互式自主，但其证据来自公开事件记录与文献综述，未提供统一实验验证。

依据：[Talk2DM: Enabling Natural Language Querying and Commonsense Reasoning for Vehicle-Road-Cloud Integrated Dynamic Maps with Large Language Models](/20251120-20261119/2602.11860v1)；[When Stopping Fails: Rethinking Minimal Risk Conditions through Human-Interactive Autonomous Driving for Safe Transportation Systems](/20251122-20261121/2606.29115v1)

## 建议阅读顺序

以下为建议学习顺序，不是公布时间排序。

1. [From Fixed Keys to Readable Schemas: Small Language Models for Vehicle Agent Function Calls](/20260822-20261119/2609.09476v2) · 入门
   - 阅读理由：从车辆功能调用这一核心任务切入，理解函数表面表示对小模型能力与失败模式的影响，建立车载工具调用的基本问题框架。
   - 公布时间：2026-09-08（日精度）
   - arxiv · 2026-09-08（日精度）：[原文](https://arxiv.org/pdf/2609.09476v2)

2. [Talk to Me, Jarvis: An Open-Source Edge-Deployable Voice Assistant Framework for Autonomous Racecars](/20251122-20261121/2609.21109v1) · 入门
   - 阅读理由：展示离线边缘语音助手从语音到高层行为命令的完整链路与延迟/准确率证据，适合作为系统实现入门案例。
   - 公布时间：2026-09-17（日精度）
   - arxiv · 2026-09-17（日精度）：[原文](https://arxiv.org/pdf/2609.21109v1)

3. [Modular Autonomy with Conversational Interaction: An LLM-driven Framework for Decision Making in Autonomous Driving](/20251122-20261121/2601.05806v1) · 入门
   - 阅读理由：以Autoware为例说明LLM交互层、DSL与安全校验如何接入模块化自动驾驶栈，帮助理解命令翻译与执行反馈。
   - 公布时间：2026-01-09（日精度）
   - arxiv · 2026-01-09（日精度）：[原文](https://arxiv.org/pdf/2601.05806v1)

4. [doPlan: A Variable-Horizon Dataset for Multi-Stage Language-Conditioned Planning in Autonomous Driving](/20251122-20261121/2609.38028v1) · 入门
   - 阅读理由：通过多阶段乘客意图数据集认识长时意图与规划窗口的错位，是理解“指令不是一次性”的关键入门材料。
   - 公布时间：2026-09-29（日精度）
   - arxiv · 2026-09-29（日精度）：[原文](https://arxiv.org/pdf/2609.38028v1)

5. [Language2Drive: Do Vision-Language-Action Models Really Follow the Instructions in Autonomous Driving?](/20251122-20261121/2610.16634v1) · 入门
   - 阅读理由：反事实配对评测揭示驾驶成功不等于语言跟随，适合在进入具体方法前建立评测批判视角。
   - 公布时间：2026-10-12（日精度）
   - arxiv · 2026-10-12（日精度）：[原文](https://arxiv.org/pdf/2610.16634v1)

6. [VehicleMemBench: An Executable Benchmark for Multi-User Long-Term Memory in In-Vehicle Agents](/20251122-20261121/2603.23840v1) · 入门
   - 阅读理由：多用户长期记忆的可执行基准，补足单轮指令之外的个人化与记忆演化问题。
   - 公布时间：2026-03-25（日精度）
   - arxiv · 2026-03-25（日精度）：[原文](https://arxiv.org/pdf/2603.23840v1)

7. [Towards Informed Autonomy Design: Understanding the Interplay of Function Characteristics and Autonomy Preferences in Automotive Agents](/20251122-20261121/2611.19474v1) · 进阶
   - 阅读理由：从功能特性到自主等级的实证研究，帮助理解主动交互中“是否执行”的设计依据与局限。
   - 公布时间：2026-11-14（日精度）
   - arxiv · 2026-11-14（日精度）：[原文](https://arxiv.org/pdf/2611.19474v1)

8. [MILD: Mediator Agentic System with Bidirectional Perception and Multi-Layered Alignment for Human-Vehicle Collaboration](/20251120-20261119/2605.01507v3) · 进阶
   - 阅读理由：中介者在环架构展示双向感知、约束对齐与可解释策略生成，适合进阶理解人车协同系统设计。
   - 公布时间：2026-05-02（日精度）
   - arxiv · 2026-05-02（日精度）：[原文](https://arxiv.org/pdf/2605.01507v3)

9. [Natural Language Instructions for Scene-Responsive Human-in-the-Loop Motion Planning in Autonomous Driving using Vision-Language-Action Models](/20251122-20261121/2602.04184v1) · 进阶
   - 阅读理由：指令条件化端到端规划的复现基线，具体展示自由指令如何进入轨迹生成及提示措辞的影响。
   - 公布时间：2026-02-04（日精度）
   - arxiv · 2026-02-04（日精度）：[原文](https://arxiv.org/pdf/2602.04184v1)

10. [Open-Ended Instruction Realization with LLM-Enabled Multi-Planner Scheduling in Autonomous Vehicles](/20251122-20261121/2604.08031v1) · 进阶
   - 阅读理由：开放指令到多MPC规划器调度的闭环框架，适合理解语义推理与控制解耦及延迟容忍设计。
   - 公布时间：2026-04-09（日精度）
   - arxiv · 2026-04-09（日精度）：[原文](https://arxiv.org/pdf/2604.08031v1)

11. [Language-Driven Cost Optimization for Autonomous Driving](/20251122-20261121/2606.10974v1) · 进阶
   - 阅读理由：语言驱动代价参数优化与人在回路确认，补充行为调整而非直接轨迹生成的另一条实现路径。
   - 公布时间：2026-06-09（日精度）
   - arxiv · 2026-06-09（日精度）：[原文](https://arxiv.org/pdf/2606.10974v1)

12. [A Large-Language-Model Supported Personalized Driving Framework for Lane Change in Highway Scenarios](/20251120-20261119/2606.31483v2) · 进阶
   - 阅读理由：个性化车道变换中自然语言偏好到规划参数的映射与RAG解释，适合理解隐式偏好处理。
   - 公布时间：2026-06-30（日精度）
   - arxiv · 2026-06-30（日精度）：[原文](https://arxiv.org/pdf/2606.31483v2)

13. [Jev with Foresight: Safe Language-Guided Autonomous Driving via a Language World Model](/20260822-20261119/2611.05448v1) · 进阶
   - 阅读理由：语言世界模型预测候选动作后果以提升安全性，展示前瞻推理与类型化决策的结合。
   - 公布时间：2026-11-03（日精度）
   - arxiv · 2026-11-03（日精度）：[原文](https://arxiv.org/pdf/2611.05448v1)

14. [From Human Intention to Action Prediction: Intention-Driven End-to-End Autonomous Driving](/20251122-20261121/2512.12302v2) · 进阶
   - 阅读理由：意图驱动端到端驾驶的任务定义与新评价协议，适合进阶理解意图满足的度量难题。
   - 公布时间：2025-12-13（日精度）
   - arxiv · 2025-12-13（日精度）：[原文](https://arxiv.org/pdf/2512.12302v2)

15. [SafeDriveVLA: Navigation-Conditioned World Model Dreaming for Conflict-Aware End-to-End Autonomous Driving](/20260822-20261119/2610.20609v1) · 进阶
   - 阅读理由：导航冲突感知与对抗鲁棒性基准及安全VLA设计，适合进阶理解开放语言接口的安全面。
   - 公布时间：2026-10-14（日精度）
   - arxiv · 2026-10-14（日精度）：[原文](https://arxiv.org/pdf/2610.20609v1)

16. [Listen, Look, Drive: Coupling Audio Instructions for User-aware VLA-based Autonomous Driving](/20251122-20261121/2601.12142v3) · 进阶
   - 阅读理由：语音指令与情感线索耦合进VLA，展示多模态在线通道对驾驶行为的影响。
   - 公布时间：2026-01-17（日精度）
   - arxiv · 2026-01-17（日精度）：[原文](https://arxiv.org/pdf/2601.12142v3)

17. [E3AD: An Emotion-Aware Vision-Language-Action Model for Human-Centric End-to-End Autonomous Driving](/20251122-20261121/2512.04733v3) · 进阶
   - 阅读理由：情感感知VLA与连续情感模型，适合进阶比较情感建模在规划与反馈中的不同用法。
   - 公布时间：2025-12-04（日精度）
   - arxiv · 2025-12-04（日精度）：[原文](https://arxiv.org/pdf/2512.04733v3)

18. [Vision-Language Assistant for Emotional Reactions to Risky Driving](/20251122-20261121/2607.16181v1) · 专题
   - 阅读理由：风险驾驶检测加情绪化语言反馈的完整管线与用户研究，适合理解情感反馈的接受度差异。
   - 公布时间：2026-07-17（日精度）
   - arxiv · 2026-07-17（日精度）：[原文](https://arxiv.org/pdf/2607.16181v1)

19. [When the Environment Becomes the Interface: Multisensory Environmental Interfaces for Human-AI Interaction in Autonomous Vehicles](/20251122-20261121/2609.32604v1) · 专题
   - 阅读理由：座舱环境作为界面的实验研究，提供非显式交互与信任线索的专题视角。
   - 公布时间：2026-09-26（日精度）
   - arxiv · 2026-09-26（日精度）：[原文](https://arxiv.org/pdf/2609.32604v1)

20. [Talk2DM: Enabling Natural Language Querying and Commonsense Reasoning for Vehicle-Road-Cloud Integrated Dynamic Maps with Large Language Models](/20251120-20261119/2602.11860v1) · 专题
   - 阅读理由：车路云动态地图的自然语言查询与常识推理，适合专题关注导航信息服务与外部基础设施协同。
   - 公布时间：2026-02-12（日精度）
   - arxiv · 2026-02-12（日精度）：[原文](https://arxiv.org/pdf/2602.11860v1)

任务：研究方向大礼包

固定窗口：arXiv &#91;2025-11-22, 2026-11-22&#41;；会议 &#91;2024-11-22, 2026-11-22&#41;（UTC，结束日不含）

本次候选评审上限 300，最终名单上限 100；本轮内容预算 10。

覆盖限制：仅检索配置范围内已有库存与预算内候选；向量/会议Top-k召回并非全库遍历，不保证找全相关论文。未核实录用、日期边界和缺失库存不能当作已覆盖。

研究需求：关注系统如何理解驾驶员或乘客的需求，结合当前情境决定是否追问、提醒或执行任务；覆盖任务型对话、主动交互、导航与出行服务、工具调用和车辆功能操作。

# in-car-agent

以下为本次固定最终名单，按相关性评分降序；不代表全部相关论文。

1. [From Fixed Keys to Readable Schemas: Small Language Models for Vehicle Agent Function Calls](https://arxiv.org/abs/2609.09476v2) · 分数 9
2. [VehicleMemBench: An Executable Benchmark for Multi-User Long-Term Memory in In-Vehicle Agents](https://arxiv.org/abs/2603.23840v1) · 分数 9
3. [Talk to Me, Jarvis: An Open-Source Edge-Deployable Voice Assistant Framework for Autonomous Racecars](https://arxiv.org/abs/2609.21109v1) · 分数 8
4. [Towards Informed Autonomy Design: Understanding the Interplay of Function Characteristics and Autonomy Preferences in Automotive Agents](https://arxiv.org/abs/2611.19474v1) · 分数 8
5. [MILD: Mediator Agentic System with Bidirectional Perception and Multi-Layered Alignment for Human-Vehicle Collaboration](https://arxiv.org/abs/2605.01507v3) · 分数 8
6. [Vision-Language Assistant for Emotional Reactions to Risky Driving](https://arxiv.org/abs/2607.16181v1) · 分数 8
7. [Modular Autonomy with Conversational Interaction: An LLM-driven Framework for Decision Making in Autonomous Driving](https://arxiv.org/abs/2601.05806v1) · 分数 8
8. [An LLM-Explainable DRL Framework for Passenger-Directed Autonomous Driving](https://arxiv.org/abs/2606.20640v1) · 分数 7
9. [doPlan: A Variable-Horizon Dataset for Multi-Stage Language-Conditioned Planning in Autonomous Driving](https://arxiv.org/abs/2609.38028v1) · 分数 7
10. [Listen, Look, Drive: Coupling Audio Instructions for User-aware VLA-based Autonomous Driving](https://arxiv.org/abs/2601.12142v3) · 分数 7
11. [A Large-Language-Model Supported Personalized Driving Framework for Lane Change in Highway Scenarios](https://arxiv.org/abs/2606.31483v2) · 分数 7
12. [Language2Drive: Do Vision-Language-Action Models Really Follow the Instructions in Autonomous Driving?](https://arxiv.org/abs/2610.16634v1) · 分数 6
13. [When the Environment Becomes the Interface: Multisensory Environmental Interfaces for Human-AI Interaction in Autonomous Vehicles](https://arxiv.org/abs/2609.32604v1) · 分数 6
14. [Jev with Foresight: Safe Language-Guided Autonomous Driving via a Language World Model](https://arxiv.org/abs/2611.05448v1) · 分数 6
15. [Talk2DM: Enabling Natural Language Querying and Commonsense Reasoning for Vehicle-Road-Cloud Integrated Dynamic Maps with Large Language Models](https://arxiv.org/abs/2602.11860v1) · 分数 6
16. [Natural Language Instructions for Scene-Responsive Human-in-the-Loop Motion Planning in Autonomous Driving using Vision-Language-Action Models](https://arxiv.org/abs/2602.04184v1) · 分数 6
17. [Open-Ended Instruction Realization with LLM-Enabled Multi-Planner Scheduling in Autonomous Vehicles](https://arxiv.org/abs/2604.08031v1) · 分数 6
18. [From Human Intention to Action Prediction: Intention-Driven End-to-End Autonomous Driving](https://arxiv.org/abs/2512.12302v2) · 分数 6
19. [Language-Driven Cost Optimization for Autonomous Driving](https://arxiv.org/abs/2606.10974v1) · 分数 6
20. [SafeDriveVLA: Navigation-Conditioned World Model Dreaming for Conflict-Aware End-to-End Autonomous Driving](https://arxiv.org/abs/2610.20609v1) · 分数 6
21. [When Stopping Fails: Rethinking Minimal Risk Conditions through Human-Interactive Autonomous Driving for Safe Transportation Systems](https://arxiv.org/abs/2606.29115v1) · 分数 6
22. [E3AD: An Emotion-Aware Vision-Language-Action Model for Human-Centric End-to-End Autonomous Driving](https://arxiv.org/abs/2512.04733v3) · 分数 6
23. [ChatPlanner: A Large Language Model Framework for Personalized Public Transit Routing](https://arxiv.org/abs/2606.15315v3) · 分数 6

[按公布时间查看](#/starter-pack/20261122-a04aee8c6135/dates)

阅读内容：已完成 20，待补充 3。
