<div class="dpr-topic-result-actions"><button type="button" data-topic-copy="docs/starter-pack/20261120-ece7ed14ca14/papers.md">复制论文清单</button> <a href="docs/starter-pack/20261120-ece7ed14ca14/papers.md" download data-no-router>下载 Markdown</a> <a href="docs/starter-pack/20261120-ece7ed14ca14/papers.json" download data-no-router>下载 JSON</a> <button type="button" data-topic-continue="20261120-ece7ed14ca14">继续生成阅读内容</button></div>

# kg-rag-agent · 入门导读

> 本导读基于所列论文的标题、摘要和已有速览，不代表已阅读全部全文。近期窗口不是完整领域史；检索不保证覆盖全部相关论文。模型导读需结合原文核验。

检索窗口：arXiv &#91;2025-11-20, 2026-11-20&#41;；会议 &#91;2024-11-20, 2026-11-20&#41;（UTC，结束日不含）

## 方向概览

本导读面向知识增强车载智能体，聚焦两条相互交织的线索：一是以知识图谱、场景图、GraphRAG 与因果/神经符号推理为代表的图结构知识增强方法，如何服务于自动驾驶与车载智能体的场景理解、决策与可解释性；二是这些知识增强链路自身的安全与可靠性问题，包括知识库投毒、检索污染、间接提示注入、图结构泄露、错误传播以及反事实鲁棒性评测。从输入论文看，研究问题可归纳为：如何在部分可观测与长尾场景下构建可靠、可追溯的场景知识表示；如何让检索到的知识真正适用于当前场景而非仅语义相关；如何评测模型是否具备因果而非语言层面的理解；以及知识增强链路在对抗与噪声条件下是否仍然可信。现有工作已给出若干具体进展，例如知识图谱增强的细粒度场景问答、来源可追溯的多车协同知识图、场景适用性风险规则推理、查询自适应的神经符号推理与多项因果/反事实评测基准；但各方法的实验设置、数据集与指标差异较大，跨工作的直接可比性有限。需要说明的是，本导读仅依据输入论文的标题、摘要与已有 TLDR 生成，未补写任何未提供的经典文献、实验数字或外部资源；输入中多数论文的 TLDR 为空，因此导读以摘要为主要证据。这是一个近期检索窗口内的入门导读，不构成该领域的完整历史综述。

依据：[KLDrive: Fine-Grained 3D Scene Reasoning for Autonomous Driving based on Knowledge Graph](/20251120-20261119/2603.21029v1)；[G-MARK: Grounded Multi-Agent Reasoning for Cooperative Driving via Knowledge Graphs](/20251120-20261119/2608.19964v1)；[KnowVal: A Knowledge-Augmented and Value-Guided Autonomous Driving System](/20251120-20261119/2512.20299v2)；[VLADriver-RAG: Retrieval-Augmented Vision-Language-Action Models for Autonomous Driving](/20251120-20261119/2605.08133v2)；[Beyond Retrieval Relevance: Scene-Grounded Risk Entailment for Vision-Language Driving](/20260822-20261119/2609.34145v1)；[DRIV-EX: Counterfactual Explanations for Driving LLMs](/20251120-20261119/2603.00696v2)；[From Scene Graphs to Answers: Selective Neuro-Symbolic Reasoning for Autonomous Driving](/20260822-20261119/2609.32645v1)；[CausalDriveBench: Evaluating Causal Reasoning in Vision-Language-Action Models for Autonomous Driving](/20260822-20261119/2609.32157v1)；[Query-Efficient Agentic Graph Extraction Attacks on GraphRAG Systems](/20251120-20261119/2601.14662v2)；[Combating Knowledge Corruption in Agent Systems: A Byzantine-Tolerant Secure Collaborative RAG Framework](/20251120-20261119/2608.04366v1)；[Integrating Graphs, Large Language Models, and Agents: Reasoning and Retrieval](/20251120-20261119/2604.15951v2)；[A Survey of Reasoning in Autonomous Driving Systems: Open Challenges and Emerging Paradigms](/20251120-20261119/2603.11093v1)

## 子方向一：场景知识图谱与结构化场景表示

这一子方向关注把多模态感知与轨迹数据转成显式、可查询、可验证的结构化知识，作为下游推理与决策的基础。KLDrive 构建能量化的场景事实知识图以支撑细粒度问答；G-MARK 把协同观测转成带来源归属、可见性与冲突信息的知识图；NIKG 提出面向自车意图上下文的 OWL 本体与构建流程；CASCADE 强调时空-因果表示与人工标注，使推理预测可逐元素机器验证；NeuroSymbEAD 提供以自车为中心的知识图与多层次文本描述数据集；Predicate 框架用确定性谓词把驾驶语义落到统一的谓词知识图。共同趋势是：从“感知输出直接喂给语言模型”转向“先构造可审计的结构化证据，再推理”。局限在于各工作本体、数据集与标注协议不统一，摘要层面难以判断跨数据集的语义一致性；多数结论依赖各自基准，横向比较证据不足。

依据：[KLDrive: Fine-Grained 3D Scene Reasoning for Autonomous Driving based on Knowledge Graph](/20251120-20261119/2603.21029v1)；[G-MARK: Grounded Multi-Agent Reasoning for Cooperative Driving via Knowledge Graphs](/20251120-20261119/2608.19964v1)；[A Semantic Knowledge Graph Construction Pipeline for Vehicle Intention Prediction in nuScenes](/20260822-20261119/2610.26528v1)；[CASCADE: A Spatio-Temporal-Causal Reasoning Representation and Dataset for Driving](/20251120-20261119/2609.07094v1)；[NeuroSymbEAD: A Large Scale Neuro-Symbolic Caption Dataset for Omni-Directional Embodied Autonomous Driving](/20260822-20261119/2609.16919v1)；[Grounding Vision-Language Models in Driving Semantics: A Multi-Dataset Predicate Framework for Explainable Reasoning](/20260822-20261119/2609.31636v1)；[Information Coordination as a Bridge: A Neuro-Symbolic Architecture for Reliable Autonomous Driving Scene Understanding](/20251120-20261119/2605.04475v1)

## 子方向二：GraphRAG 与图检索增强的推理机制

这一子方向研究如何从图中检索“最小且充分”的证据并组织成推理路径。相关输入包括：路径约束检索 PCR 用图结构约束限制检索空间以保证推理链一致；GFM-Retriever 以图基础模型做跨域子图检索并用信息瓶颈选子图；INSES 针对噪声稀疏图做 LLM 引导导航与相似度扩展；GraphScout 训练模型自主探索图；FlowRAG 用多粒度异构图与频率感知流提取显式推理路径；EAGR 在隐式语义图上做证据引导的自适应扩展；A2RAG 与 PathRouter 分别从成本自适应与路径级奖励对齐角度改进入图检索智能体；ArcRAG 关注检索策略跨图构建方式的可移植性；Typed-Centrality 与 FoG 分别引入符号中心性与证据覆盖奖励。综述类输入（图-LLM-智能体整合综述）提供了按目的、图模态与整合策略分类的框架。总体看，研究重心正从“检索相关内容”转向“检索可支撑结论的证据路径”，并开始关注成本、可移植性与证据可审计性。局限是这些方法多在通用多跳问答基准上验证，摘要中未见其在车载实时约束下的系统评估。

依据：[Path-Constrained Retrieval: A Structural Approach to Reliable LLM Agent Reasoning Through Graph-Scoped Semantic Search](/20251120-20261119/2511.18313v1)；[Retrieving Minimal and Sufficient Reasoning Subgraphs with Graph Foundation Models for Path-aware GraphRAG](/20251120-20261119/2603.07179v1)；[Beyond Explicit Edges: Robust Reasoning over Noisy and Sparse Knowledge Graphs](/20251120-20261119/2603.14006v2)；[GraphScout: Empowering Large Language Models with Intrinsic Exploration Ability for Agentic Graph Reasoning](/20251120-20261119/2603.01410v2)；[FlowRAG: Synergizing Explicit Reasoning via Frequency-Aware Multi-Granularity Graph Flow](/20251120-20261119/2606.17856v1)；[EAGR: Evidence-Guided Adaptive Graph Retrieval](/20251120-20261119/2611.01910v1)；[A2RAG: Adaptive Agentic Graph Retrieval for Cost-Aware and Reliable Reasoning](/20251120-20261119/2601.21162v2)；[PathRouter: Aligning Rewards with Retrieval Quality in Agentic Graph Retrieval-Augmented Generation](/20251120-20261119/2606.16409v1)；[ArcRAG: Agentic Compositional Retrieval over Knowledge Graphs](/20251120-20261119/2611.06481v1)；[Typed-Centrality Grounding for Agentic GraphRAG: A Symbolic Approach for Agentic Reasoning](/20251120-20261119/2611.09414v1)；[Clearing the FoG: Training KG Agents to Retrieve the Evidence Behind Their Answers](/20251120-20261119/2610.37405v1)；[Integrating Graphs, Large Language Models, and Agents: Reasoning and Retrieval](/20251120-20261119/2604.15951v2)；[GraphWalk: Enabling Reasoning in Large Language Models through Tool-Based Graph Navigation](/20251120-20261119/2604.01610v1)；[Grounding LLM Reasoning under Incomplete Graph Evidence](/20251120-20261119/2606.30247v1)

## 子方向三：因果推理、反事实与神经符号决策

这一子方向讨论如何让车载智能体的推理具备因果结构与可验证性。CausalDriveBench 基于因果层级构造因果问答与反事实轨迹，用于检验 VLA 的因果理解；DRIV-EX 用反事实解释识别改变驾驶决策的最小语义改动；CF-VLA 在动作执行前做反事实自省并修正元动作；CASCADE 提供带因果链接的人工标注表示；CoG 以关系蓝图与失败感知回溯做可控图推理；选择性神经符号框架让符号执行优先、语言模型仅处理无法精确求解的查询；双过程规划用结构化思维链与规则校验器保证推理-动作一致；开放世界双过程方法用知识图推理上下文风险并在两种规划间切换；FOL 语义通信在协同场景中做逻辑演绎；LA-RL 与 SARAD 把语言/检索知识与强化学习或安全约束结合。值得警惕的是，有输入明确指出反事实推理可能只是语言捷径而非真正的因果理解，这提示该子方向的评测必须区分“说得对”与“想得对”。摘要层面尚无法判断各方法的因果结论在分布外场景的稳定性。

依据：[CausalDriveBench: Evaluating Causal Reasoning in Vision-Language-Action Models for Autonomous Driving](/20260822-20261119/2609.32157v1)；[DRIV-EX: Counterfactual Explanations for Driving LLMs](/20251120-20261119/2603.00696v2)；[Counterfactual VLA: Self-Reflective Vision-Language-Action Model with Adaptive Reasoning](/20251120-20261119/2512.24426v1)；[CASCADE: A Spatio-Temporal-Causal Reasoning Representation and Dataset for Driving](/20251120-20261119/2609.07094v1)；[CoG: Controllable Graph Reasoning via Relational Blueprints and Failure-Aware Refinement over Knowledge Graphs](/20251120-20261119/2601.11047v2)；[From Scene Graphs to Answers: Selective Neuro-Symbolic Reasoning for Autonomous Driving](/20260822-20261119/2609.32645v1)；[Cognitive Dual-Process Planning for Autonomous Driving with Structured Scene Knowledge and Verifiable Reasoning-Action Consistency](/20251120-20261119/2607.19194v2)；[Towards Safer Autonomous Driving in an Open World: A Dual-Process Approach](/20260822-20261119/2610.04088v1)；[Goal-Oriented Logic-based Semantic Communication for Neuro-Symbolic Reasoning with Applications onto Autonomous Driving](/20251120-20261119/2608.00878v1)；[LA-RL: Language Action-guided Reinforcement Learning with Safety Guarantees for Autonomous Highway Driving](/20251120-20261119/2512.05686v1)；[SARAD: LLM-Based Safety-Aware Hybrid Reinforcement Learning with Collision Prediction for Autonomous Driving](/20251120-20261119/2605.28583v1)；[Teaching VLMs What to Say, Not How to Reason: Rethinking Counterfactual Reasoning in Autonomous Driving](/20260822-20261119/2611.24376v1)；[ActMem: Bridging the Gap Between Memory Retrieval and Reasoning in LLM Agents](/20251120-20261119/2603.00026v2)

## 子方向四：知识增强驾驶智能体的决策与规划集成

这一子方向关注知识、检索与推理如何真正接入规划与控制回路。KnowVal 用驾驶知识图加检索与价值模型做轨迹评估；VLADriver-RAG 把感知抽象为时空语义图并做场景对齐检索；场景适用性风险推理把检索相关性升级为规则可适用性；分层记忆与工具调用框架把短期场景状态与长期经验结合；AD-Memo 用语言化记忆扩展思维链；SteerVLA 用语言指令引导底层驾驶策略；轻量置信度感知与 LUNA-AD 用蒸馏与终身学习降低推理开销；DriveFoundry 与 DrivingAgent 关注数据-模型闭环与智能体化调度；AutoDrive-P3 与 FastDriveCoT 关注结构化思维链及其加速。共同问题是推理延迟与安全关键实时性之间的张力，以及知识注入是否真正改变底层行为而非仅改变解释文本。多数摘要报告的是各自基准上的结果，跨方法的统一评测证据不足。

依据：[KnowVal: A Knowledge-Augmented and Value-Guided Autonomous Driving System](/20251120-20261119/2512.20299v2)；[VLADriver-RAG: Retrieval-Augmented Vision-Language-Action Models for Autonomous Driving](/20251120-20261119/2605.08133v2)；[Beyond Retrieval Relevance: Scene-Grounded Risk Entailment for Vision-Language Driving](/20260822-20261119/2609.34145v1)；[Drive by Hindsight and Foresight: Tool-Grounded Synergistic Reasoning over Hierarchical Memory for Autonomous Driving](/20260822-20261119/2609.08217v1)；[Vision-Language-Action Autonomous Driving Agent with Language-based Memory](/20260822-20261119/2609.38641v1)；[SteerVLA: Steering Vision-Language-Action Models in Long-Tail Driving Scenarios](/20251120-20261119/2602.08440v2)；[Decision-Making with Lightweight Confidence-Aware Language Model for Autonomous Driving](/20251120-20261119/2605.25393v1)；[LUNA-AD: Lightweight Uncertainty-Aware Language Model with Lifelong Learning for Autonomous Driving](/20251120-20261119/2606.08470v1)；[DriveFoundry: Co-Evolving Data and Model for Efficient Closed-Loop Iteration in Autonomous Driving](/20260822-20261119/2611.11532v1)；[DrivingAgent: Design and Scheduling Agents for Autonomous Driving Systems](/20251120-20261119/2606.12236v2)；[&#36;AutoDrive&#92;text&#123;-&#125;P^3&#36;: Unified Chain of Perception-Prediction-Planning Thought via Reinforcement Fine-Tuning](/20251120-20261119/2603.28116v1)；[Accelerating Structured Chain-of-Thought in Autonomous Vehicles](/20251120-20261119/2602.02864v1)；[A Survey of Reasoning in Autonomous Driving Systems: Open Challenges and Emerging Paradigms](/20251120-20261119/2603.11093v1)

## 子方向五：知识库投毒、检索污染与智能体信息安全

这一子方向直接对应知识增强链路的安全风险。AGEA 研究在查询预算约束下对 GraphRAG 隐藏图结构的智能体化抽取攻击，说明图检索系统可能泄露实体关系结构；SecureCollaRAG 针对 RAG 文档投毒提出拜占庭容错的多源可信度校验；Ctrl-G 关注把图证据发送给远程模型时的结构暴露与交互暴露累积；NeuroTaint 面向 LLM 智能体的信息流追踪，覆盖间接提示注入与跨会话记忆持久化；不完整图证据下的接地理论分析指出，在开放世界不完整下不存在既能拒绝所有错误轨迹又保留所有真但未观测轨迹的硬规则，这为知识增强系统的可靠性边界提供了形式化视角；对抗视觉感知评测则提示感知层攻击可导致驾驶分数大幅下降。需要注意：输入中直接针对车载知识库投毒与检索污染的专门工作较少，多数安全证据来自通用 GraphRAG 或智能体安全场景，向车载场景迁移的有效性在摘要层面无法确认。

依据：[Query-Efficient Agentic Graph Extraction Attacks on GraphRAG Systems](/20251120-20261119/2601.14662v2)；[Combating Knowledge Corruption in Agent Systems: A Byzantine-Tolerant Secure Collaborative RAG Framework](/20251120-20261119/2608.04366v1)；[Ctrl-G: Controlling Structural and Interaction Exposure in Knowledge Graph Augmented LLM Reasoning](/20251120-20261119/2601.08739v2)；[Ghost in the Agent: Redefining Information Flow Tracking for LLM Agents](/20251120-20261119/2604.23374v1)；[Grounding LLM Reasoning under Incomplete Graph Evidence](/20251120-20261119/2606.30247v1)；[AD&#36;^2&#36;: Analysis and Detection of Adversarial Threats in Visual Perception for End-to-End Autonomous Driving Systems](/20251120-20261119/2602.10160v1)；[Integrating Graphs, Large Language Models, and Agents: Reasoning and Retrieval](/20251120-20261119/2604.15951v2)

## 子方向六：评测基准、鲁棒性与错误传播

这一子方向提供衡量进展与暴露局限的手段。CausalDriveBench 检验因果问答与反事实轨迹；DriveSpatial 用动态多关系场景图构造跨视角与时空推理题；Drive-P2D 采用推理与答案分离的渐进式感知到决策评测；DriveCombo 评测组合交通规则推理与规则冲突；TAD 聚焦长短时驾驶视频的时序理解；CoLT-Drive 用反事实长尾基准测决策级可负担动作预测；AnchorReasoning 与 GRAVA 提供视觉接地推理数据与表示；跨阶段一致性协议用 NLI 矛盾率衡量感知-预测-规划的一致性；K-Risk 提供高风险场景的知识增强标注数据；CRASH 用真实事故报告做原因归因；DriveSpatial 等基准普遍显示模型与人类存在明显差距。关于错误传播，输入中多为间接证据（如跨阶段矛盾、推理捷径、图证据不完整），尚缺乏对“检索污染如何在多跳推理中逐级放大”的专门量化研究，这一点应明确标注为证据不足。

依据：[CausalDriveBench: Evaluating Causal Reasoning in Vision-Language-Action Models for Autonomous Driving](/20260822-20261119/2609.32157v1)；[DRIVESPATIAL: A Benchmark for Spatiotemporal Intelligence in VLMs for Autonomous Driving](/20251120-20261119/2605.23176v3)；[Drive-P2D: A Progressive Perception-to-Decision Benchmark for VLMs in Autonomous Driving](/20251120-20261119/2601.14702v2)；[DriveCombo: Benchmarking Compositional Traffic Rule Reasoning in Autonomous Driving](/20251120-20261119/2603.01637v1)；[From Segments to Scenes: Temporal Understanding for Agentic Autonomous Driving via Vision-Language Models](/20251120-20261119/2512.05277v4)；[CoLT-Drive: Counterfactual Long-Tail Benchmarking and Knowledge-Preserving Adaptation for Driving Affordance Prediction](/20260822-20261119/2609.00242v1)；[AnchorReasoning: A Visual Grounding and Causal Reasoning Dataset in Long-Tail Autonomous Driving Scenarios](/20260822-20261119/2609.28366v1)；[GRAVA: Grounded Reasoning-to-Action Representation and Learning for Autonomous Driving](/20260822-20261119/2609.15169v1)；[Cross-Stage Coherence in Hierarchical Driving VQA: A Consistency Protocol and Parameter-Efficient Gated Context Routing](/20251120-20261119/2604.22560v2)；[A knowledge-augmented dataset of high-risk driving scenarios with LLM annotations for autonomous driving](/20251120-20261119/2607.07103v1)；[CRASH: Cognitive Reasoning Agent for Safety Hazards in Autonomous Driving](/20251120-20261119/2603.15364v1)；[Grounding LLM Reasoning under Incomplete Graph Evidence](/20251120-20261119/2606.30247v1)

## 子方向七：车载交互、个性化与协同知识服务

这一子方向把知识增强从单车决策扩展到人车协同与车路云协同。Talk2DM 为车路云动态地图提供自然语言查询与常识推理；个性化换道框架用 RAG 把自然语言偏好映射为可执行规划参数；交互式决策框架用对象-过程建模与语言化外部人机接口提升混合交通中的可理解性；MILD 以中介智能体整合舱内舱外感知与约束加权策略优化；智能体化 MPC 用语言智能体在运行时重合成控制规范；语义通信工作把一阶逻辑证据在车路间按目标导向选择性传输；协同潜空间推理框架在通信预算下做非对称语义协同。这些工作共同表明知识增强不仅服务于“车怎么开”，也服务于“人如何理解与干预车”。局限在于多数验证在仿真或离线数据上，真实部署中的延迟、隐私与跨主体信任问题在摘要层面讨论有限。

依据：[Talk2DM: Enabling Natural Language Querying and Commonsense Reasoning for Vehicle-Road-Cloud Integrated Dynamic Maps with Large Language Models](/20251120-20261119/2602.11860v1)；[A Large-Language-Model Supported Personalized Driving Framework for Lane Change in Highway Scenarios](/20251120-20261119/2606.31483v2)；[Large Language Model based Interactive Decision-Making for Autonomous Driving](/20251120-20261119/2604.23513v1)；[MILD: Mediator Agentic System with Bidirectional Perception and Multi-Layered Alignment for Human-Vehicle Collaboration](/20251120-20261119/2605.01507v3)；[Agentic MPC for Semantic Control System Resynthesis](/20251120-20261119/2606.12774v1)；[Goal-Oriented Logic-based Semantic Communication for Neuro-Symbolic Reasoning with Applications onto Autonomous Driving](/20251120-20261119/2608.00878v1)；[DH-VLM: Dual-Horizon Cooperative Latent Reasoning for Autonomous Driving](/20251120-20261119/2608.09333v1)

## 进展与局限总结

进展方面：场景知识表示从通用场景图走向带来源、可见性、冲突与因果链接的可审计结构；图检索从语义相似走向证据路径、结构约束与成本自适应；推理侧出现符号优先、语言补位的选择性神经符号范式；评测侧出现因果层级、跨视角时空、组合规则与反事实长尾等多维基准；安全侧已识别图结构抽取、文档投毒、信息流泄露与不完整证据下的可靠性边界等问题。局限方面：其一，本体、数据集与指标不统一，跨工作可比性弱；其二，多数方法在摘要中未报告车载实时约束下的系统级延迟与资源开销；其三，因果与反事实推理可能退化为语言捷径，现有证据提示需要区分解释文本与真实因果结构；其四，专门面向车载知识库投毒与检索污染的工作在输入中较少，安全结论多来自通用场景；其五，错误传播的逐级量化证据不足。以上局限均基于输入摘要可观察到的范围，未做外部补充。

依据：[KLDrive: Fine-Grained 3D Scene Reasoning for Autonomous Driving based on Knowledge Graph](/20251120-20261119/2603.21029v1)；[G-MARK: Grounded Multi-Agent Reasoning for Cooperative Driving via Knowledge Graphs](/20251120-20261119/2608.19964v1)；[Beyond Retrieval Relevance: Scene-Grounded Risk Entailment for Vision-Language Driving](/20260822-20261119/2609.34145v1)；[From Scene Graphs to Answers: Selective Neuro-Symbolic Reasoning for Autonomous Driving](/20260822-20261119/2609.32645v1)；[CausalDriveBench: Evaluating Causal Reasoning in Vision-Language-Action Models for Autonomous Driving](/20260822-20261119/2609.32157v1)；[Teaching VLMs What to Say, Not How to Reason: Rethinking Counterfactual Reasoning in Autonomous Driving](/20260822-20261119/2611.24376v1)；[Query-Efficient Agentic Graph Extraction Attacks on GraphRAG Systems](/20251120-20261119/2601.14662v2)；[Combating Knowledge Corruption in Agent Systems: A Byzantine-Tolerant Secure Collaborative RAG Framework](/20251120-20261119/2608.04366v1)；[Grounding LLM Reasoning under Incomplete Graph Evidence](/20251120-20261119/2606.30247v1)；[A Survey of Reasoning in Autonomous Driving Systems: Open Challenges and Emerging Paradigms](/20251120-20261119/2603.11093v1)；[Beyond Textual Chain-of-Thought: A Survey on Action-Grounded Reasoning in Autonomous Driving](/20251120-20261119/2609.01659v1)

## 建议阅读顺序

以下为建议学习顺序，不是公布时间排序。

1. [A Survey of Reasoning in Autonomous Driving Systems: Open Challenges and Emerging Paradigms](/20251120-20261119/2603.11093v1) · 入门
   - 阅读理由：先建立领域问题框架：该综述提出认知层级与七类推理挑战，并指出延迟与安全的关键张力，适合作为入门地图。
   - 公布时间：2026-03-11（日精度）
   - arxiv · 2026-03-11（日精度）：[原文](https://arxiv.org/pdf/2603.11093v1)

2. [Integrating Graphs, Large Language Models, and Agents: Reasoning and Retrieval](/20251120-20261119/2604.15951v2) · 入门
   - 阅读理由：补充图-LLM-智能体整合的设计空间分类，帮助理解后续方法在目的、图模态与整合策略上的位置。
   - 公布时间：2026-04-17（日精度）
   - arxiv · 2026-04-17（日精度）：[原文](https://arxiv.org/pdf/2604.15951v2)

3. [KLDrive: Fine-Grained 3D Scene Reasoning for Autonomous Driving based on Knowledge Graph](/20251120-20261119/2603.21029v1) · 入门
   - 阅读理由：知识图谱增强场景问答的代表性框架，可先看结构化场景事实如何支撑推理。
   - 公布时间：2026-03-22（日精度）
   - arxiv · 2026-03-22（日精度）：[原文](https://arxiv.org/pdf/2603.21029v1)

4. [A Semantic Knowledge Graph Construction Pipeline for Vehicle Intention Prediction in nuScenes](/20260822-20261119/2610.26528v1) · 入门
   - 阅读理由：本体化意图知识图的构建流程，适合理解场景知识如何被显式建模与验证。
   - 公布时间：2026-10-19（日精度）
   - arxiv · 2026-10-19（日精度）：[原文](https://arxiv.org/pdf/2610.26528v1)

5. [CASCADE: A Spatio-Temporal-Causal Reasoning Representation and Dataset for Driving](/20251120-20261119/2609.07094v1) · 进阶
   - 阅读理由：时空-因果表示与人工标注数据集，连接场景表示与可验证推理。
   - 公布时间：2026-09-07（日精度）
   - arxiv · 2026-09-07（日精度）：[原文](https://arxiv.org/pdf/2609.07094v1)

6. [G-MARK: Grounded Multi-Agent Reasoning for Cooperative Driving via Knowledge Graphs](/20251120-20261119/2608.19964v1) · 进阶
   - 阅读理由：多车协同下带来源归属与冲突的知识图，展示知识增强在部分可观测场景的价值。
   - 公布时间：2026-08-20（日精度）
   - arxiv · 2026-08-20（日精度）：[原文](https://arxiv.org/pdf/2608.19964v1)

7. [Path-Constrained Retrieval: A Structural Approach to Reliable LLM Agent Reasoning Through Graph-Scoped Semantic Search](/20251120-20261119/2511.18313v1) · 进阶
   - 阅读理由：路径约束检索是理解“结构化检索保证推理一致”的清晰入口。
   - 公布时间：2025-11-23（日精度）
   - arxiv · 2025-11-23（日精度）：[原文](https://arxiv.org/pdf/2511.18313v1)

8. [Retrieving Minimal and Sufficient Reasoning Subgraphs with Graph Foundation Models for Path-aware GraphRAG](/20251120-20261119/2603.07179v1) · 进阶
   - 阅读理由：子图检索与信息瓶颈选择，理解最小充分证据的检索思路。
   - 公布时间：2026-03-07（日精度）
   - arxiv · 2026-03-07（日精度）：[原文](https://arxiv.org/pdf/2603.07179v1)

9. [Beyond Explicit Edges: Robust Reasoning over Noisy and Sparse Knowledge Graphs](/20251120-20261119/2603.14006v2) · 进阶
   - 阅读理由：面向噪声稀疏图的动态检索，补充真实知识图不完整时的应对。
   - 公布时间：2026-03-14（日精度）
   - arxiv · 2026-03-14（日精度）：[原文](https://arxiv.org/pdf/2603.14006v2)

10. [FlowRAG: Synergizing Explicit Reasoning via Frequency-Aware Multi-Granularity Graph Flow](/20251120-20261119/2606.17856v1) · 进阶
   - 阅读理由：多粒度图与显式路径提取，展示检索如何产出可解释推理骨架。
   - 公布时间：2026-06-16（日精度）
   - arxiv · 2026-06-16（日精度）：[原文](https://arxiv.org/pdf/2606.17856v1)

11. [From Scene Graphs to Answers: Selective Neuro-Symbolic Reasoning for Autonomous Driving](/20260822-20261119/2609.32645v1) · 进阶
   - 阅读理由：查询自适应神经符号推理，是符号执行与语言推理分工的代表。
   - 公布时间：2026-09-26（日精度）
   - arxiv · 2026-09-26（日精度）：[原文](https://arxiv.org/pdf/2609.32645v1)

12. [CoG: Controllable Graph Reasoning via Relational Blueprints and Failure-Aware Refinement over Knowledge Graphs](/20251120-20261119/2601.11047v2) · 进阶
   - 阅读理由：关系蓝图与失败感知回溯，理解可控图推理与推理停滞处理。
   - 公布时间：2026-01-16（日精度）
   - arxiv · 2026-01-16（日精度）：[原文](https://arxiv.org/pdf/2601.11047v2)

13. [Beyond Retrieval Relevance: Scene-Grounded Risk Entailment for Vision-Language Driving](/20260822-20261119/2609.34145v1) · 进阶
   - 阅读理由：从检索相关性到场景适用性，直接对应知识增强中的适用性缺口。
   - 公布时间：2026-09-28（日精度）
   - arxiv · 2026-09-28（日精度）：[原文](https://arxiv.org/pdf/2609.34145v1)

14. [KnowVal: A Knowledge-Augmented and Value-Guided Autonomous Driving System](/20251120-20261119/2512.20299v2) · 进阶
   - 阅读理由：知识图加检索与价值模型接入规划的完整链路，适合看知识如何影响轨迹评估。
   - 公布时间：2025-12-23（日精度）
   - arxiv · 2025-12-23（日精度）：[原文](https://arxiv.org/pdf/2512.20299v2)

15. [VLADriver-RAG: Retrieval-Augmented Vision-Language-Action Models for Autonomous Driving](/20251120-20261119/2605.08133v2) · 进阶
   - 阅读理由：时空语义图与场景对齐检索用于 VLA 规划，连接检索与端到端驾驶。
   - 公布时间：2026-05-01（日精度）
   - arxiv · 2026-05-01（日精度）：[原文](https://arxiv.org/pdf/2605.08133v2)

16. [CausalDriveBench: Evaluating Causal Reasoning in Vision-Language-Action Models for Autonomous Driving](/20260822-20261119/2609.32157v1) · 专题
   - 阅读理由：因果层级评测基准，是判断因果理解是否真实的关键工具。
   - 公布时间：2026-09-26（日精度）
   - arxiv · 2026-09-26（日精度）：[原文](https://arxiv.org/pdf/2609.32157v1)

17. [Teaching VLMs What to Say, Not How to Reason: Rethinking Counterfactual Reasoning in Autonomous Driving](/20260822-20261119/2611.24376v1) · 专题
   - 阅读理由：对反事实推理是否只是语言捷径的批判性分析，用于校准对因果方法的期待。
   - 公布时间：2026-11-18（日精度）
   - arxiv · 2026-11-18（日精度）：[原文](https://arxiv.org/pdf/2611.24376v1)

18. [Query-Efficient Agentic Graph Extraction Attacks on GraphRAG Systems](/20251120-20261119/2601.14662v2) · 专题
   - 阅读理由：GraphRAG 图结构抽取攻击，理解知识图检索系统的结构泄露风险。
   - 公布时间：2026-01-21（日精度）
   - arxiv · 2026-01-21（日精度）：[原文](https://arxiv.org/pdf/2601.14662v2)

19. [Combating Knowledge Corruption in Agent Systems: A Byzantine-Tolerant Secure Collaborative RAG Framework](/20251120-20261119/2608.04366v1) · 专题
   - 阅读理由：RAG 文档投毒与拜占庭容错校验，对应知识库投毒威胁。
   - 公布时间：2026-08-05（日精度）
   - arxiv · 2026-08-05（日精度）：[原文](https://arxiv.org/pdf/2608.04366v1)

20. [Ghost in the Agent: Redefining Information Flow Tracking for LLM Agents](/20251120-20261119/2604.23374v1) · 专题
   - 阅读理由：智能体信息流追踪，覆盖间接提示注入与跨会话污染，补足安全视角。
   - 公布时间：2026-04-25（日精度）
   - arxiv · 2026-04-25（日精度）：[原文](https://arxiv.org/pdf/2604.23374v1)

任务：研究方向大礼包

固定窗口：arXiv &#91;2025-11-20, 2026-11-20&#41;；会议 &#91;2024-11-20, 2026-11-20&#41;（UTC，结束日不含）

本次候选评审上限 300，最终名单上限 100；本轮内容预算 10。

覆盖限制：仅检索配置范围内已有库存与预算内候选；向量/会议Top-k召回并非全库遍历，不保证找全相关论文。未核实录用、日期边界和缺失库存不能当作已覆盖。

缺失库存：eccv 2025、emnlp 2026、neurips 2026。

研究需求：面向知识增强车载智能体，重点关注知识图谱、GraphRAG、因果推理等图结构方法在车载智能体领域的应用，以及知识库投毒、检索污染、间接提示注入、错误传播与反事实鲁棒性评测等人工智能安全方向。

# kg-rag-agent

以下为本次固定最终名单，按相关性评分降序；不代表全部相关论文。

1. [KLDrive: Fine-Grained 3D Scene Reasoning for Autonomous Driving based on Knowledge Graph](https://arxiv.org/abs/2603.21029v1) · 分数 9
2. [G-MARK: Grounded Multi-Agent Reasoning for Cooperative Driving via Knowledge Graphs](https://arxiv.org/abs/2608.19964v1) · 分数 9
3. [KnowVal: A Knowledge-Augmented and Value-Guided Autonomous Driving System](https://arxiv.org/abs/2512.20299v2) · 分数 9
4. [VLADriver-RAG: Retrieval-Augmented Vision-Language-Action Models for Autonomous Driving](https://arxiv.org/abs/2605.08133v2) · 分数 8
5. [Beyond Retrieval Relevance: Scene-Grounded Risk Entailment for Vision-Language Driving](https://arxiv.org/abs/2609.34145v1) · 分数 8
6. [DRIV-EX: Counterfactual Explanations for Driving LLMs](https://arxiv.org/abs/2603.00696v2) · 分数 8
7. [DH-VLM: Dual-Horizon Cooperative Latent Reasoning for Autonomous Driving](https://arxiv.org/abs/2608.09333v1) · 分数 8
8. [From Scene Graphs to Answers: Selective Neuro-Symbolic Reasoning for Autonomous Driving](https://arxiv.org/abs/2609.32645v1) · 分数 8
9. [Cognitive Dual-Process Planning for Autonomous Driving with Structured Scene Knowledge and Verifiable Reasoning-Action Consistency](https://arxiv.org/abs/2607.19194v2) · 分数 8
10. [CausalDriveBench: Evaluating Causal Reasoning in Vision-Language-Action Models for Autonomous Driving](https://arxiv.org/abs/2609.32157v1) · 分数 8
11. [SteerVLA: Steering Vision-Language-Action Models in Long-Tail Driving Scenarios](https://arxiv.org/abs/2602.08440v2) · 分数 8
12. [Query-Efficient Agentic Graph Extraction Attacks on GraphRAG Systems](https://arxiv.org/abs/2601.14662v2) · 分数 7
13. [Stateful Multi-Agent LLMs for Cross-View Interface Alignment in Automotive Model-Based Systems Engineering](https://arxiv.org/abs/2608.08038v1) · 分数 7
14. [Decision-Making with Lightweight Confidence-Aware Language Model for Autonomous Driving](https://arxiv.org/abs/2605.25393v1) · 分数 7
15. [A Semantic Knowledge Graph Construction Pipeline for Vehicle Intention Prediction in nuScenes](https://arxiv.org/abs/2610.26528v1) · 分数 7
16. [Retrieval-Augmented Large Language Model Decision-Making for Autonomous Driving Guided by Chinese Philosophical Wisdom](https://arxiv.org/abs/2610.03948v3) · 分数 7
17. [Path-Constrained Retrieval: A Structural Approach to Reliable LLM Agent Reasoning Through Graph-Scoped Semantic Search](https://arxiv.org/abs/2511.18313v1) · 分数 7
18. [Drive by Hindsight and Foresight: Tool-Grounded Synergistic Reasoning over Hierarchical Memory for Autonomous Driving](https://arxiv.org/abs/2609.08217v1) · 分数 7
19. [A Survey of Reasoning in Autonomous Driving Systems: Open Challenges and Emerging Paradigms](https://arxiv.org/abs/2603.11093v1) · 分数 7
20. [Grounding Vision-Language Models in Driving Semantics: A Multi-Dataset Predicate Framework for Explainable Reasoning](https://arxiv.org/abs/2609.31636v1) · 分数 7
21. [A Large-Language-Model Supported Personalized Driving Framework for Lane Change in Highway Scenarios](https://arxiv.org/abs/2606.31483v2) · 分数 7
22. [Large Language Model based Interactive Decision-Making for Autonomous Driving](https://arxiv.org/abs/2604.23513v1) · 分数 7
23. [MILD: Mediator Agentic System with Bidirectional Perception and Multi-Layered Alignment for Human-Vehicle Collaboration](https://arxiv.org/abs/2605.01507v3) · 分数 7
24. [Towards Safer Autonomous Driving in an Open World: A Dual-Process Approach](https://arxiv.org/abs/2610.04088v1) · 分数 7
25. [CASCADE: A Spatio-Temporal-Causal Reasoning Representation and Dataset for Driving](https://arxiv.org/abs/2609.07094v1) · 分数 7
26. [Ghost in the Agent: Redefining Information Flow Tracking for LLM Agents](https://arxiv.org/abs/2604.23374v1) · 分数 7
27. [Vision-Language-Action Autonomous Driving Agent with Language-based Memory](https://arxiv.org/abs/2609.38641v1) · 分数 7
28. [Goal-Oriented Logic-based Semantic Communication for Neuro-Symbolic Reasoning with Applications onto Autonomous Driving](https://arxiv.org/abs/2608.00878v1) · 分数 7
29. [Counterfactual VLA: Self-Reflective Vision-Language-Action Model with Adaptive Reasoning](https://arxiv.org/abs/2512.24426v1) · 分数 7
30. [CoLT-Drive: Counterfactual Long-Tail Benchmarking and Knowledge-Preserving Adaptation for Driving Affordance Prediction](https://arxiv.org/abs/2609.00242v1) · 分数 7
31. [AnchorReasoning: A Visual Grounding and Causal Reasoning Dataset in Long-Tail Autonomous Driving Scenarios](https://arxiv.org/abs/2609.28366v1) · 分数 7
32. [GRAVA: Grounded Reasoning-to-Action Representation and Learning for Autonomous Driving](https://arxiv.org/abs/2609.15169v1) · 分数 7
33. [Talk2DM: Enabling Natural Language Querying and Commonsense Reasoning for Vehicle-Road-Cloud Integrated Dynamic Maps with Large Language Models](https://arxiv.org/abs/2602.11860v1) · 分数 7
34. [Teaching VLMs What to Say, Not How to Reason: Rethinking Counterfactual Reasoning in Autonomous Driving](https://arxiv.org/abs/2611.24376v1) · 分数 7
35. [CRASH: Cognitive Reasoning Agent for Safety Hazards in Autonomous Driving](https://arxiv.org/abs/2603.15364v1) · 分数 7
36. [Typed-Centrality Grounding for Agentic GraphRAG: A Symbolic Approach for Agentic Reasoning](https://arxiv.org/abs/2611.09414v1) · 分数 6
37. [ArcRAG: Agentic Compositional Retrieval over Knowledge Graphs](https://arxiv.org/abs/2611.06481v1) · 分数 6
38. [Clearing the FoG: Training KG Agents to Retrieve the Evidence Behind Their Answers](https://arxiv.org/abs/2610.37405v1) · 分数 6
39. [Ctrl-G: Controlling Structural and Interaction Exposure in Knowledge Graph Augmented LLM Reasoning](https://arxiv.org/abs/2601.08739v2) · 分数 6
40. [Beyond Explicit Edges: Robust Reasoning over Noisy and Sparse Knowledge Graphs](https://arxiv.org/abs/2603.14006v2) · 分数 6
41. [GraphScout: Empowering Large Language Models with Intrinsic Exploration Ability for Agentic Graph Reasoning](https://arxiv.org/abs/2603.01410v2) · 分数 6
42. [FlowRAG: Synergizing Explicit Reasoning via Frequency-Aware Multi-Granularity Graph Flow](https://arxiv.org/abs/2606.17856v1) · 分数 6
43. [Retrieving Minimal and Sufficient Reasoning Subgraphs with Graph Foundation Models for Path-aware GraphRAG](https://arxiv.org/abs/2603.07179v1) · 分数 6
44. [EvoGraph-R1: Self-Evolving Multimodal Knowledge Hypergraphs for Agentic Retrieval](https://arxiv.org/abs/2607.12764v1) · 分数 6
45. [A2RAG: Adaptive Agentic Graph Retrieval for Cost-Aware and Reliable Reasoning](https://arxiv.org/abs/2601.21162v2) · 分数 6
46. [PathRouter: Aligning Rewards with Retrieval Quality in Agentic Graph Retrieval-Augmented Generation](https://arxiv.org/abs/2606.16409v1) · 分数 6
47. [Knowledge Is Not Static: Order-Aware Hypergraph RAG for Language Models](https://arxiv.org/abs/2604.12185v1) · 分数 6
48. [RouterKGQA: Specialized--General Model Routing for Constraint-Aware Knowledge Graph Question Answering](https://arxiv.org/abs/2603.20017v1) · 分数 6
49. [EAGR: Evidence-Guided Adaptive Graph Retrieval](https://arxiv.org/abs/2611.01910v1) · 分数 6
50. [Combating Knowledge Corruption in Agent Systems: A Byzantine-Tolerant Secure Collaborative RAG Framework](https://arxiv.org/abs/2608.04366v1) · 分数 6
51. [PatternBloom: Empowering Agentic RAG with Externalized RL-Distilled Graph Patterns](https://arxiv.org/abs/2611.10477v1) · 分数 6
52. [KG-Reasoner: A Reinforced Model for End-to-End Multi-Hop Knowledge Graph Reasoning](https://arxiv.org/abs/2604.12487v1) · 分数 6
53. [Chat2Scenic: An Iterative RAG-Based Framework for Scenario Generation in Autonomous Driving](https://arxiv.org/abs/2607.14387v1) · 分数 6
54. [A knowledge-augmented dataset of high-risk driving scenarios with LLM annotations for autonomous driving](https://arxiv.org/abs/2607.07103v1) · 分数 6
55. [Integrating Graphs, Large Language Models, and Agents: Reasoning and Retrieval](https://arxiv.org/abs/2604.15951v2) · 分数 6
56. [GraphWalk: Enabling Reasoning in Large Language Models through Tool-Based Graph Navigation](https://arxiv.org/abs/2604.01610v1) · 分数 6
57. [Grounding LLM Reasoning under Incomplete Graph Evidence](https://arxiv.org/abs/2606.30247v1) · 分数 6
58. [RouteRAG: Efficient Retrieval-Augmented Generation from Text and Graph via Reinforcement Learning](https://arxiv.org/abs/2512.09487v1) · 分数 6
59. [HyperGraphPro: Progress-Aware Reinforcement Learning for Structure-Guided Hypergraph RAG](https://arxiv.org/abs/2601.17755v3) · 分数 6
60. [SCOUT-RAG: Scalable and Cost-Efficient Unifying Traversal for Agentic Graph-RAG over Distributed Domains](https://arxiv.org/abs/2602.08400v1) · 分数 6
61. [RESPOND: Risk-Enhanced Structured Pattern for LLM-driven Online Node-level Decision-making](https://arxiv.org/abs/2512.20179v1) · 分数 6
62. [LA-RL: Language Action-guided Reinforcement Learning with Safety Guarantees for Autonomous Highway Driving](https://arxiv.org/abs/2512.05686v1) · 分数 6
63. [SARAD: LLM-Based Safety-Aware Hybrid Reinforcement Learning with Collision Prediction for Autonomous Driving](https://arxiv.org/abs/2605.28583v1) · 分数 6
64. [STEM: Structure-Tracing Evidence Mining for Knowledge Graphs-Driven Retrieval-Augmented Generation](https://arxiv.org/abs/2604.22282v2) · 分数 6
65. [Topology-Aware Reasoning over Incomplete Knowledge Graph with Graph-Based Soft Prompting](https://arxiv.org/abs/2604.12503v2) · 分数 6
66. [CoG: Controllable Graph Reasoning via Relational Blueprints and Failure-Aware Refinement over Knowledge Graphs](https://arxiv.org/abs/2601.11047v2) · 分数 6
67. [Teaching LLMs to See Graphs: Unifying Text and Structural Reasoning](https://arxiv.org/abs/2605.10247v2) · 分数 6
68. [KG-ASG: Collision-Knowledge-Guided Closed-Loop Adversarial Scenario Generation With Primary-Support Attribution](https://arxiv.org/abs/2605.18895v1) · 分数 6
69. [Interactive Structured Environment Scaling for Large Language Model Agentic Reasoning](https://arxiv.org/abs/2611.19871v1) · 分数 6
70. [ActMem: Bridging the Gap Between Memory Retrieval and Reasoning in LLM Agents](https://arxiv.org/abs/2603.00026v2) · 分数 6
71. [Cross-Stage Coherence in Hierarchical Driving VQA: A Consistency Protocol and Parameter-Efficient Gated Context Routing](https://arxiv.org/abs/2604.22560v2) · 分数 6
72. [LMGenDrive: Bridging Multimodal Understanding and Generative World Modeling for End-to-End Driving](https://arxiv.org/abs/2604.08719v1) · 分数 6
73. [Information Coordination as a Bridge: A Neuro-Symbolic Architecture for Reliable Autonomous Driving Scene Understanding](https://arxiv.org/abs/2605.04475v1) · 分数 6
74. [From Segments to Scenes: Temporal Understanding for Agentic Autonomous Driving via Vision-Language Models](https://arxiv.org/abs/2512.05277v4) · 分数 6
75. [LUNA-AD: Lightweight Uncertainty-Aware Language Model with Lifelong Learning for Autonomous Driving](https://arxiv.org/abs/2606.08470v1) · 分数 6
76. [DriveFoundry: Co-Evolving Data and Model for Efficient Closed-Loop Iteration in Autonomous Driving](https://arxiv.org/abs/2611.11532v1) · 分数 6
77. [DrivingAgent: Design and Scheduling Agents for Autonomous Driving Systems](https://arxiv.org/abs/2606.12236v2) · 分数 6
78. [&#36;AutoDrive&#92;text&#123;-&#125;P^3&#36;: Unified Chain of Perception-Prediction-Planning Thought via Reinforcement Fine-Tuning](https://arxiv.org/abs/2603.28116v1) · 分数 6
79. [Agentic MPC for Semantic Control System Resynthesis](https://arxiv.org/abs/2606.12774v1) · 分数 6
80. [Time is Not a Label: Continuous Phase Rotation for Temporal Knowledge Graphs and Agentic Memory](https://arxiv.org/abs/2604.11544v2) · 分数 6
81. [NeuroSymbEAD: A Large Scale Neuro-Symbolic Caption Dataset for Omni-Directional Embodied Autonomous Driving](https://arxiv.org/abs/2609.16919v1) · 分数 6
82. [PlannerForge: LLM Agents for Scenario-Based Testing of Motion Planners in Autonomous Driving](https://arxiv.org/abs/2609.08965v1) · 分数 6
83. [Accelerating Structured Chain-of-Thought in Autonomous Vehicles](https://arxiv.org/abs/2602.02864v1) · 分数 6
84. [AD&#36;^2&#36;: Analysis and Detection of Adversarial Threats in Visual Perception for End-to-End Autonomous Driving Systems](https://arxiv.org/abs/2602.10160v1) · 分数 6
85. [DRIVESPATIAL: A Benchmark for Spatiotemporal Intelligence in VLMs for Autonomous Driving](https://arxiv.org/abs/2605.23176v3) · 分数 6
86. [Leveraging LLM-GNN Integration for Open-World Question Answering over Knowledge Graphs](https://arxiv.org/abs/2604.13979v1) · 分数 6
87. [TuringPAI: A Foundation for On-Device Physical AI](https://arxiv.org/abs/2611.25474v1) · 分数 6
88. [Frozen LLMs as Map-Aware Spatio-Temporal Reasoners for Vehicle Trajectory Prediction](https://arxiv.org/abs/2604.21479v3) · 分数 6
89. [Unifying Language-Action Understanding and Generation for Autonomous Driving](https://arxiv.org/abs/2603.01441v1) · 分数 6
90. [AutoMoT: A Unified Vision-Language-Action Model with Asynchronous Mixture-of-Transformers for End-to-End Autonomous Driving](https://arxiv.org/abs/2603.14851v3) · 分数 6
91. [Beyond Textual Chain-of-Thought: A Survey on Action-Grounded Reasoning in Autonomous Driving](https://arxiv.org/abs/2609.01659v1) · 分数 6
92. [Drive-P2D: A Progressive Perception-to-Decision Benchmark for VLMs in Autonomous Driving](https://arxiv.org/abs/2601.14702v2) · 分数 6
93. [CARLA-GS: Decoupling Representation, Reasoning, and Physics Simulation for Autonomous Driving Corner-Case Synthesis](https://arxiv.org/abs/2607.07601v1) · 分数 6
94. [DriveCombo: Benchmarking Compositional Traffic Rule Reasoning in Autonomous Driving](https://arxiv.org/abs/2603.01637v1) · 分数 6
95. [LAD-Drive: Bridging Language and Trajectory with Action-Aware Diffusion Transformers](https://arxiv.org/abs/2603.02035v1) · 分数 6
96. [VILTA: A VLM-in-the-Loop Adversary for Enhancing Driving Policy Robustness](https://arxiv.org/abs/2601.12672v1) · 分数 6

[按公布时间查看](#/starter-pack/20261120-ece7ed14ca14/dates)

阅读内容：已完成 18，待补充 78。
