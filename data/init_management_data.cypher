// 管理学知识图谱初始化脚本
// 所有标签使用 glx_ 前缀

// ==================== 清除旧数据 ====================
MATCH (n:glx_Module) DETACH DELETE n;
MATCH (n:glx_Chapter) DETACH DELETE n;
MATCH (n:glx_Knowledge) DETACH DELETE n;
MATCH (n:glx_Ability) DETACH DELETE n;

// ==================== 模块节点 ====================
CREATE (m1:glx_Module {id: 'M1', name: '管理基础理论', description: '管理的基本概念、职能和管理者的角色与技能'})
CREATE (m2:glx_Module {id: 'M2', name: '决策与计划', description: '决策的过程和方法，计划工作的制定与实施'})
CREATE (m3:glx_Module {id: 'M3', name: '战略管理', description: '企业战略分析、制定和实施的过程和方法'})
CREATE (m4:glx_Module {id: 'M4', name: '组织管理', description: '组织结构设计、文化建设和权力分配'})
CREATE (m5:glx_Module {id: 'M5', name: '控制与创新', description: '企业的控制管理和创新发展战略'})

// ==================== 章节节点 ====================
// 模块1 - 管理基础理论
CREATE (c1_1:glx_Chapter {id: 'C1_1', name: '管理基础', module_id: 'M1', description: '管理是一门重要的学科，涉及对人力、物资和信息资源的有效协调和利用，实现组织目标。理解管理的核心概念和职能是学习管理学的基础。'})
CREATE (c1_2:glx_Chapter {id: 'C1_2', name: '管理思想', module_id: 'M1', description: '不同时期和学派的管理思想各有侧重。从科学管理到行为科学理论，反映了管理思想的演变和发展，揭示了管理的本质。'})

// 模块2 - 决策与计划
CREATE (c2_1:glx_Chapter {id: 'C2_1', name: '决策管理', module_id: 'M2', description: '决策是管理的核心职能，贯穿于管理工作的全过程。有效的决策需要科学的方法和合理的程序，包括定性和定量方法。'})
CREATE (c2_2:glx_Chapter {id: 'C2_2', name: '计划工作', module_id: 'M2', description: '计划是指挥其他管理职能的基础。战略规划需要充分分析内外部环境，制定合适的发展方向。'})

// 模块3 - 战略管理
CREATE (c3_1:glx_Chapter {id: 'C3_1', name: '战略分析', module_id: 'M3', description: '战略分析工具帮助企业准确把握自身优劣势和外部机遇与威胁，为战略决策提供重要参考。'})
CREATE (c3_2:glx_Chapter {id: 'C3_2', name: '战略选择', module_id: 'M3', description: '企业需根据自身条件选择合适的竞争战略，并确保战略得到有效实施，实现组织目标。'})

// 模块4 - 组织管理
CREATE (c4_1:glx_Chapter {id: 'C4_1', name: '组织设计', module_id: 'M4', description: '组织结构是为实现企业目标而设计的。合理的组织设计需要明确权力结构和沟通机制。'})
CREATE (c4_2:glx_Chapter {id: 'C4_2', name: '组织运作', module_id: 'M4', description: '组织的有效运作需要良好的沟通、有凝聚力的团队和适当的激励措施，调动员工的积极性。'})

// 模块5 - 控制与创新
CREATE (c5_1:glx_Chapter {id: 'C5_1', name: '控制管理', module_id: 'M5', description: '控制是确保战略实施和目标实现的重要保障，包括绩效评估、质量管理和成本控制。'})
CREATE (c5_2:glx_Chapter {id: 'C5_2', name: '创新发展', module_id: 'M5', description: '创新是企业保持竞争力的关键。企业需要建立知识管理体系，鼓励创新，优化供应链，承担社会责任。'})

// ==================== 知识点节点 ====================
// 模块1 - 管理基础
CREATE (k1:glx_Knowledge {id: 'KP_M1_C1_1', name: '管理的概念', chapter_id: 'C1_1', description: '管理是指在特定的环境下，组织协调他人，通过计划、组织、领导和控制等职能实现目标的过程。', difficulty: '基础'})
CREATE (k2:glx_Knowledge {id: 'KP_M1_C1_2', name: '管理的职能', chapter_id: 'C1_1', description: '包括计划、组织、领导和控制四大职能。计划确定目标，组织整合资源，领导协调活动，控制监督绩效。', difficulty: '基础'})
CREATE (k3:glx_Knowledge {id: 'KP_M1_C1_3', name: '管理者角色', chapter_id: 'C1_1', description: '根据明茨伯格的研究，管理者需扮演信息角色、决策角色和人际关系角色，不同层级侧重不同。', difficulty: '中等'})

// 模块1 - 管理思想
CREATE (k4:glx_Knowledge {id: 'KP_M1_C2_1', name: '科学管理理论', chapter_id: 'C1_2', description: '泰勒提出的理论强调标准化、时间研究、工作分解，通过科学方法提高效率。其核心是用科学取代经验。', difficulty: '中等'})
CREATE (k5:glx_Knowledge {id: 'KP_M1_C2_2', name: '一般管理理论', chapter_id: 'C1_2', description: '法约尔提出的理论强调管理的普遍性原理，包括计划、组织、命令、协调和控制五大职能。', difficulty: '中等'})
CREATE (k6:glx_Knowledge {id: 'KP_M1_C2_3', name: '官僚组织理论', chapter_id: 'C1_2', description: '韦伯提出的理论强调规则、等级制度和制度化，认为理性组织的前提是规范化管理。', difficulty: '中等'})
CREATE (k7:glx_Knowledge {id: 'KP_M1_C2_4', name: '行为科学理论', chapter_id: 'C1_2', description: '强调人的需求、心理和社会因素对组织行为的影响，转变了对员工的看法。', difficulty: '中等'})

// 模块2 - 决策管理
CREATE (k8:glx_Knowledge {id: 'KP_M2_C1_1', name: '决策的过程', chapter_id: 'C2_1', description: '包括确定问题、收集信息、提出方案、评估比较、选择方案和实施控制等阶段。', difficulty: '基础'})
CREATE (k9:glx_Knowledge {id: 'KP_M2_C1_2', name: '定性决策方法', chapter_id: 'C2_1', description: '包括头脑风暴法、德尔菲法、名义小组法等，基于专家经验和判断。', difficulty: '中等'})
CREATE (k10:glx_Knowledge {id: 'KP_M2_C1_3', name: '定量决策方法', chapter_id: 'C2_1', description: '包括线性规划、决策树、概率论等数学方法，追求最优决策。', difficulty: '困难'})
CREATE (k11:glx_Knowledge {id: 'KP_M2_C1_4', name: '群体决策', chapter_id: 'C2_1', description: '通过多人参与进行决策，优点是信息完整，缺点是耗时较长。', difficulty: '中等'})

// 模块2 - 计划工作
CREATE (k12:glx_Knowledge {id: 'KP_M2_C2_1', name: '计划的特征', chapter_id: 'C2_2', description: '目的性、主观性、灵活性、前瞻性，计划指导组织的其他职能。', difficulty: '基础'})
CREATE (k13:glx_Knowledge {id: 'KP_M2_C2_2', name: '战略环境分析', chapter_id: 'C2_2', description: '包括外部环境（政治、经济、社会、技术）和内部环境分析，为战略制定提供基础。', difficulty: '中等'})
CREATE (k14:glx_Knowledge {id: 'KP_M2_C2_3', name: 'SWOT分析', chapter_id: 'C2_2', description: '优势、劣势、机会和威胁分析，帮助企业清楚地认识自身状况和外部环境。', difficulty: '中等'})

// 模块3 - 战略分析
CREATE (k15:glx_Knowledge {id: 'KP_M3_C1_1', name: '波特五力模型', chapter_id: 'C3_1', description: '分析产业吸引力的模型，包括供应商、购买者、竞争对手、替代品和潜在进入者的力量。', difficulty: '中等'})

// 模块3 - 战略选择
CREATE (k16:glx_Knowledge {id: 'KP_M3_C2_1', name: '竞争战略', chapter_id: 'C3_2', description: '包括成本领先战略、差异化战略和集中化战略，企业需根据自身条件选择。', difficulty: '中等'})
CREATE (k17:glx_Knowledge {id: 'KP_M3_C2_2', name: '战略实施', chapter_id: 'C3_2', description: '通过组织设计、资源配置、绩效管理等方式确保战略的有效执行。', difficulty: '困难'})

// 模块4 - 组织设计
CREATE (k18:glx_Knowledge {id: 'KP_M4_C1_1', name: '组织结构', chapter_id: 'C4_1', description: '规定了组织成员的分工、权力关系和协调机制，常见的有职能制、事业部制和矩阵制。', difficulty: '中等'})
CREATE (k19:glx_Knowledge {id: 'KP_M4_C1_2', name: '组织文化', chapter_id: 'C4_1', description: '企业成员共同的价值观、信念和行为准则，是组织的灵魂和核心竞争力之一。', difficulty: '中等'})
CREATE (k20:glx_Knowledge {id: 'KP_M4_C1_3', name: '权力分析', chapter_id: 'C4_1', description: '权力来源包括法定权、奖励权、强制权、专家权和参考权，管理者需要合理运用。', difficulty: '中等'})

// 模块4 - 组织运作
CREATE (k21:glx_Knowledge {id: 'KP_M4_C2_1', name: '管理沟通', chapter_id: 'C4_2', description: '是信息流动的过程，包括正式和非正式沟通，有效沟通对组织运作至关重要。', difficulty: '基础'})
CREATE (k22:glx_Knowledge {id: 'KP_M4_C2_2', name: '团队建设', chapter_id: 'C4_2', description: '通过共同的目标、良好的沟通和相互信任形成团队，提高组织的整体效能。', difficulty: '中等'})
CREATE (k23:glx_Knowledge {id: 'KP_M4_C2_3', name: '员工激励', chapter_id: 'C4_2', description: '基于需要理论，包括物质激励和精神激励，合理激励能提升员工的积极性。', difficulty: '中等'})

// 模块5 - 控制管理
CREATE (k24:glx_Knowledge {id: 'KP_M5_C1_1', name: '绩效管理', chapter_id: 'C5_1', description: '包括目标设定、过程监控、结果评价和反馈改进，是控制职能的重要体现。', difficulty: '中等'})
CREATE (k25:glx_Knowledge {id: 'KP_M5_C1_2', name: '质量管理', chapter_id: 'C5_1', description: '通过制定标准、过程控制、持续改进等方法确保产品或服务的质量。', difficulty: '中等'})
CREATE (k26:glx_Knowledge {id: 'KP_M5_C1_3', name: '成本控制', chapter_id: 'C5_1', description: '通过预算、成本分析、费用审批等方式控制企业成本，提高经济效益。', difficulty: '中等'})

// 模块5 - 创新发展
CREATE (k27:glx_Knowledge {id: 'KP_M5_C2_1', name: '知识管理', chapter_id: 'C5_2', description: '企业收集、整理、共享和利用知识资源的过程，是数字化时代的重要管理内容。', difficulty: '中等'})
CREATE (k28:glx_Knowledge {id: 'KP_M5_C2_2', name: '创新管理', chapter_id: 'C5_2', description: '鼓励和支持员工的创意，通过组织创新、产品创新、管理创新驱动企业发展。', difficulty: '困难'})
CREATE (k29:glx_Knowledge {id: 'KP_M5_C2_3', name: '供应链管理', chapter_id: 'C5_2', description: '整合从原材料到最终用户的所有活动，优化资源配置，提升企业竞争力。', difficulty: '困难'})
CREATE (k30:glx_Knowledge {id: 'KP_M5_C2_4', name: '企业社会责任', chapter_id: 'C5_2', description: '企业对社会、员工、环境等方面的责任和承诺，是现代企业的重要标志。', difficulty: '中等'})

// ==================== 模块-章节关系 ====================
CREATE (m1)-[:CONTAINS]->(c1_1)
CREATE (m1)-[:CONTAINS]->(c1_2)
CREATE (m2)-[:CONTAINS]->(c2_1)
CREATE (m2)-[:CONTAINS]->(c2_2)
CREATE (m3)-[:CONTAINS]->(c3_1)
CREATE (m3)-[:CONTAINS]->(c3_2)
CREATE (m4)-[:CONTAINS]->(c4_1)
CREATE (m4)-[:CONTAINS]->(c4_2)
CREATE (m5)-[:CONTAINS]->(c5_1)
CREATE (m5)-[:CONTAINS]->(c5_2)

// ==================== 章节-知识点关系 ====================
CREATE (c1_1)-[:CONTAINS]->(k1)
CREATE (c1_1)-[:CONTAINS]->(k2)
CREATE (c1_1)-[:CONTAINS]->(k3)
CREATE (c1_2)-[:CONTAINS]->(k4)
CREATE (c1_2)-[:CONTAINS]->(k5)
CREATE (c1_2)-[:CONTAINS]->(k6)
CREATE (c1_2)-[:CONTAINS]->(k7)
CREATE (c2_1)-[:CONTAINS]->(k8)
CREATE (c2_1)-[:CONTAINS]->(k9)
CREATE (c2_1)-[:CONTAINS]->(k10)
CREATE (c2_1)-[:CONTAINS]->(k11)
CREATE (c2_2)-[:CONTAINS]->(k12)
CREATE (c2_2)-[:CONTAINS]->(k13)
CREATE (c2_2)-[:CONTAINS]->(k14)
CREATE (c3_1)-[:CONTAINS]->(k15)
CREATE (c3_2)-[:CONTAINS]->(k16)
CREATE (c3_2)-[:CONTAINS]->(k17)
CREATE (c4_1)-[:CONTAINS]->(k18)
CREATE (c4_1)-[:CONTAINS]->(k19)
CREATE (c4_1)-[:CONTAINS]->(k20)
CREATE (c4_2)-[:CONTAINS]->(k21)
CREATE (c4_2)-[:CONTAINS]->(k22)
CREATE (c4_2)-[:CONTAINS]->(k23)
CREATE (c5_1)-[:CONTAINS]->(k24)
CREATE (c5_1)-[:CONTAINS]->(k25)
CREATE (c5_1)-[:CONTAINS]->(k26)
CREATE (c5_2)-[:CONTAINS]->(k27)
CREATE (c5_2)-[:CONTAINS]->(k28)
CREATE (c5_2)-[:CONTAINS]->(k29)
CREATE (c5_2)-[:CONTAINS]->(k30)

// ==================== 知识点前置关系 ====================
CREATE (k1)-[:PREREQUISITE]->(k2)
CREATE (k2)-[:PREREQUISITE]->(k3)
CREATE (k4)-[:PREREQUISITE]->(k5)
CREATE (k8)-[:PREREQUISITE]->(k9)
CREATE (k8)-[:PREREQUISITE]->(k10)
CREATE (k13)-[:PREREQUISITE]->(k15)
CREATE (k15)-[:PREREQUISITE]->(k16)
CREATE (k16)-[:PREREQUISITE]->(k17)
CREATE (k18)-[:PREREQUISITE]->(k19)
CREATE (k21)-[:PREREQUISITE]->(k22)
CREATE (k22)-[:PREREQUISITE]->(k23)
CREATE (k24)-[:PREREQUISITE]->(k25)
CREATE (k27)-[:PREREQUISITE]->(k28)
