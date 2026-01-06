#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分批导入管理学知识图谱数据
解决大量数据一次性导入可能的超时问题
"""

from neo4j import GraphDatabase
import time

# Neo4j 连接配置
NEO4J_URI = "bolt://47.110.83.32:11001"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "mima123456"

def execute_batch(session, batch_name, statements):
    """执行一批 Cypher 语句"""
    print(f"\n{'='*60}")
    print(f"开始执行批次: {batch_name}")
    print(f"{'='*60}")
    
    success_count = 0
    for i, statement in enumerate(statements, 1):
        try:
            result = session.run(statement)
            result.consume()
            success_count += 1
            print(f"  ✅ 语句 {i}/{len(statements)} 执行成功")
        except Exception as e:
            print(f"  ❌ 语句 {i}/{len(statements)} 执行失败: {str(e)}")
    
    print(f"\n批次 '{batch_name}' 完成: {success_count}/{len(statements)} 条语句成功")
    return success_count

def main():
    print("=" * 60)
    print("管理学知识图谱数据 - 分批导入工具")
    print("=" * 60)
    
    try:
        driver = GraphDatabase.driver(
            NEO4J_URI,
            auth=(NEO4J_USER, NEO4J_PASSWORD),
            connection_timeout=10
        )
        
        with driver.session() as session:
            print("\n✅ Neo4j 连接成功!")
            
            # 第1批：创建模块节点
            batch1 = [
                "MERGE (m:glx_Module {id: 'M1', name: '管理基础理论', description: '介绍管理的基本概念、理论和历史发展'});",
                "MERGE (m:glx_Module {id: 'M2', name: '决策与计划', description: '学习组织决策过程和战略计划制定方法'});",
                "MERGE (m:glx_Module {id: 'M3', name: '战略管理', description: '深入学习企业战略分析、制定与实施'});",
                "MERGE (m:glx_Module {id: 'M4', name: '组织管理', description: '学习组织结构设计、人力资源管理与领导'});",
                "MERGE (m:glx_Module {id: 'M5', name: '控制与创新', description: '学习管理控制系统和组织创新管理'});"
            ]
            execute_batch(session, "模块节点创建", batch1)
            time.sleep(1)
            
            # 第2批：创建章节节点（前5个）
            batch2 = [
                "MERGE (c:glx_Chapter {id: 'C1_1', name: '管理概述', module_id: 'M1'});",
                "MERGE (c:glx_Chapter {id: 'C1_2', name: '管理理论发展', module_id: 'M1'});",
                "MERGE (c:glx_Chapter {id: 'C2_1', name: '决策基础', module_id: 'M2'});",
                "MERGE (c:glx_Chapter {id: 'C2_2', name: '计划管理', module_id: 'M2'});",
                "MERGE (c:glx_Chapter {id: 'C3_1', name: '战略分析', module_id: 'M3'});"
            ]
            execute_batch(session, "章节节点创建（1-5）", batch2)
            time.sleep(1)
            
            # 第3批：创建章节节点（后5个）
            batch3 = [
                "MERGE (c:glx_Chapter {id: 'C3_2', name: '战略选择与实施', module_id: 'M3'});",
                "MERGE (c:glx_Chapter {id: 'C4_1', name: '组织设计', module_id: 'M4'});",
                "MERGE (c:glx_Chapter {id: 'C4_2', name: '领导与激励', module_id: 'M4'});",
                "MERGE (c:glx_Chapter {id: 'C5_1', name: '管理控制', module_id: 'M5'});",
                "MERGE (c:glx_Chapter {id: 'C5_2', name: '创新管理', module_id: 'M5'});"
            ]
            execute_batch(session, "章节节点创建（6-10）", batch3)
            time.sleep(1)
            
            # 第4批：创建知识点（1-10）
            batch4 = [
                "MERGE (k:glx_Knowledge {id: 'k1', name: '管理的概念', difficulty: 1, chapter_id: 'C1_1'});",
                "MERGE (k:glx_Knowledge {id: 'k2', name: '管理的职能', difficulty: 2, chapter_id: 'C1_1'});",
                "MERGE (k:glx_Knowledge {id: 'k3', name: '管理者角色', difficulty: 2, chapter_id: 'C1_1'});",
                "MERGE (k:glx_Knowledge {id: 'k4', name: '管理的性质', difficulty: 2, chapter_id: 'C1_1'});",
                "MERGE (k:glx_Knowledge {id: 'k5', name: '科学管理理论', difficulty: 2, chapter_id: 'C1_2'});",
                "MERGE (k:glx_Knowledge {id: 'k6', name: '行为科学理论', difficulty: 2, chapter_id: 'C1_2'});",
                "MERGE (k:glx_Knowledge {id: 'k7', name: '系统管理理论', difficulty: 3, chapter_id: 'C1_2'});",
                "MERGE (k:glx_Knowledge {id: 'k8', name: '权变管理理论', difficulty: 3, chapter_id: 'C1_2'});",
                "MERGE (k:glx_Knowledge {id: 'k9', name: '决策的概念与类型', difficulty: 2, chapter_id: 'C2_1'});",
                "MERGE (k:glx_Knowledge {id: 'k10', name: '决策的过程', difficulty: 2, chapter_id: 'C2_1'});"
            ]
            execute_batch(session, "知识点创建（1-10）", batch4)
            time.sleep(1)
            
            # 第5批：创建知识点（11-20）
            batch5 = [
                "MERGE (k:glx_Knowledge {id: 'k11', name: '决策方法与工具', difficulty: 3, chapter_id: 'C2_1'});",
                "MERGE (k:glx_Knowledge {id: 'k12', name: '计划的类型', difficulty: 2, chapter_id: 'C2_2'});",
                "MERGE (k:glx_Knowledge {id: 'k13', name: '目标管理', difficulty: 3, chapter_id: 'C2_2'});",
                "MERGE (k:glx_Knowledge {id: 'k14', name: '计划编制方法', difficulty: 3, chapter_id: 'C2_2'});",
                "MERGE (k:glx_Knowledge {id: 'k15', name: '战略管理过程', difficulty: 3, chapter_id: 'C3_1'});",
                "MERGE (k:glx_Knowledge {id: 'k16', name: 'SWOT分析', difficulty: 2, chapter_id: 'C3_1'});",
                "MERGE (k:glx_Knowledge {id: 'k17', name: '波特五力模型', difficulty: 3, chapter_id: 'C3_1'});",
                "MERGE (k:glx_Knowledge {id: 'k18', name: '公司层战略', difficulty: 3, chapter_id: 'C3_2'});",
                "MERGE (k:glx_Knowledge {id: 'k19', name: '业务层战略', difficulty: 3, chapter_id: 'C3_2'});",
                "MERGE (k:glx_Knowledge {id: 'k20', name: '战略实施与控制', difficulty: 4, chapter_id: 'C3_2'});"
            ]
            execute_batch(session, "知识点创建（11-20）", batch5)
            time.sleep(1)
            
            # 第6批：创建知识点（21-30）
            batch6 = [
                "MERGE (k:glx_Knowledge {id: 'k21', name: '组织结构设计', difficulty: 3, chapter_id: 'C4_1'});",
                "MERGE (k:glx_Knowledge {id: 'k22', name: '组织文化', difficulty: 3, chapter_id: 'C4_1'});",
                "MERGE (k:glx_Knowledge {id: 'k23', name: '组织变革', difficulty: 4, chapter_id: 'C4_1'});",
                "MERGE (k:glx_Knowledge {id: 'k24', name: '领导理论', difficulty: 3, chapter_id: 'C4_2'});",
                "MERGE (k:glx_Knowledge {id: 'k25', name: '激励理论', difficulty: 3, chapter_id: 'C4_2'});",
                "MERGE (k:glx_Knowledge {id: 'k26', name: '团队管理', difficulty: 3, chapter_id: 'C4_2'});",
                "MERGE (k:glx_Knowledge {id: 'k27', name: '控制的过程', difficulty: 2, chapter_id: 'C5_1'});",
                "MERGE (k:glx_Knowledge {id: 'k28', name: '绩效管理', difficulty: 3, chapter_id: 'C5_1'});",
                "MERGE (k:glx_Knowledge {id: 'k29', name: '创新的类型', difficulty: 2, chapter_id: 'C5_2'});",
                "MERGE (k:glx_Knowledge {id: 'k30', name: '创新管理实践', difficulty: 4, chapter_id: 'C5_2'});"
            ]
            execute_batch(session, "知识点创建（21-30）", batch6)
            time.sleep(1)
            
            # 第7批：创建模块-章节关系
            batch7 = [
                "MATCH (m:glx_Module {id: 'M1'}), (c:glx_Chapter) WHERE c.module_id = 'M1' MERGE (m)-[:HAS_CHAPTER]->(c);",
                "MATCH (m:glx_Module {id: 'M2'}), (c:glx_Chapter) WHERE c.module_id = 'M2' MERGE (m)-[:HAS_CHAPTER]->(c);",
                "MATCH (m:glx_Module {id: 'M3'}), (c:glx_Chapter) WHERE c.module_id = 'M3' MERGE (m)-[:HAS_CHAPTER]->(c);",
                "MATCH (m:glx_Module {id: 'M4'}), (c:glx_Chapter) WHERE c.module_id = 'M4' MERGE (m)-[:HAS_CHAPTER]->(c);",
                "MATCH (m:glx_Module {id: 'M5'}), (c:glx_Chapter) WHERE c.module_id = 'M5' MERGE (m)-[:HAS_CHAPTER]->(c);"
            ]
            execute_batch(session, "模块-章节关系创建", batch7)
            time.sleep(1)
            
            # 第8批：创建章节-知识点关系
            batch8 = [
                "MATCH (c:glx_Chapter), (k:glx_Knowledge) WHERE k.chapter_id = c.id MERGE (c)-[:HAS_KNOWLEDGE]->(k);"
            ]
            execute_batch(session, "章节-知识点关系创建", batch8)
            time.sleep(1)
            
            # 第9批：创建知识点前置关系（1-15）
            batch9 = [
                "MATCH (k1:glx_Knowledge {id: 'k1'}), (k2:glx_Knowledge {id: 'k2'}) MERGE (k1)-[:PREREQUISITE]->(k2);",
                "MATCH (k1:glx_Knowledge {id: 'k1'}), (k3:glx_Knowledge {id: 'k3'}) MERGE (k1)-[:PREREQUISITE]->(k3);",
                "MATCH (k2:glx_Knowledge {id: 'k2'}), (k4:glx_Knowledge {id: 'k4'}) MERGE (k2)-[:PREREQUISITE]->(k4);",
                "MATCH (k1:glx_Knowledge {id: 'k1'}), (k5:glx_Knowledge {id: 'k5'}) MERGE (k1)-[:PREREQUISITE]->(k5);",
                "MATCH (k5:glx_Knowledge {id: 'k5'}), (k6:glx_Knowledge {id: 'k6'}) MERGE (k5)-[:PREREQUISITE]->(k6);",
                "MATCH (k6:glx_Knowledge {id: 'k6'}), (k7:glx_Knowledge {id: 'k7'}) MERGE (k6)-[:PREREQUISITE]->(k7);",
                "MATCH (k7:glx_Knowledge {id: 'k7'}), (k8:glx_Knowledge {id: 'k8'}) MERGE (k7)-[:PREREQUISITE]->(k8);",
                "MATCH (k2:glx_Knowledge {id: 'k2'}), (k9:glx_Knowledge {id: 'k9'}) MERGE (k2)-[:PREREQUISITE]->(k9);",
                "MATCH (k9:glx_Knowledge {id: 'k9'}), (k10:glx_Knowledge {id: 'k10'}) MERGE (k9)-[:PREREQUISITE]->(k10);",
                "MATCH (k10:glx_Knowledge {id: 'k10'}), (k11:glx_Knowledge {id: 'k11'}) MERGE (k10)-[:PREREQUISITE]->(k11);",
                "MATCH (k9:glx_Knowledge {id: 'k9'}), (k12:glx_Knowledge {id: 'k12'}) MERGE (k9)-[:PREREQUISITE]->(k12);",
                "MATCH (k12:glx_Knowledge {id: 'k12'}), (k13:glx_Knowledge {id: 'k13'}) MERGE (k12)-[:PREREQUISITE]->(k13);",
                "MATCH (k12:glx_Knowledge {id: 'k12'}), (k14:glx_Knowledge {id: 'k14'}) MERGE (k12)-[:PREREQUISITE]->(k14);",
                "MATCH (k11:glx_Knowledge {id: 'k11'}), (k15:glx_Knowledge {id: 'k15'}) MERGE (k11)-[:PREREQUISITE]->(k15);",
                "MATCH (k15:glx_Knowledge {id: 'k15'}), (k16:glx_Knowledge {id: 'k16'}) MERGE (k15)-[:PREREQUISITE]->(k16);"
            ]
            execute_batch(session, "知识点前置关系创建（1-15）", batch9)
            time.sleep(1)
            
            # 第10批：创建知识点前置关系（16-25）
            batch10 = [
                "MATCH (k16:glx_Knowledge {id: 'k16'}), (k17:glx_Knowledge {id: 'k17'}) MERGE (k16)-[:PREREQUISITE]->(k17);",
                "MATCH (k16:glx_Knowledge {id: 'k16'}), (k18:glx_Knowledge {id: 'k18'}) MERGE (k16)-[:PREREQUISITE]->(k18);",
                "MATCH (k17:glx_Knowledge {id: 'k17'}), (k19:glx_Knowledge {id: 'k19'}) MERGE (k17)-[:PREREQUISITE]->(k19);",
                "MATCH (k18:glx_Knowledge {id: 'k18'}), (k20:glx_Knowledge {id: 'k20'}) MERGE (k18)-[:PREREQUISITE]->(k20);",
                "MATCH (k19:glx_Knowledge {id: 'k19'}), (k20:glx_Knowledge {id: 'k20'}) MERGE (k19)-[:PREREQUISITE]->(k20);",
                "MATCH (k4:glx_Knowledge {id: 'k4'}), (k21:glx_Knowledge {id: 'k21'}) MERGE (k4)-[:PREREQUISITE]->(k21);",
                "MATCH (k21:glx_Knowledge {id: 'k21'}), (k22:glx_Knowledge {id: 'k22'}) MERGE (k21)-[:PREREQUISITE]->(k22);",
                "MATCH (k22:glx_Knowledge {id: 'k22'}), (k23:glx_Knowledge {id: 'k23'}) MERGE (k22)-[:PREREQUISITE]->(k23);",
                "MATCH (k3:glx_Knowledge {id: 'k3'}), (k24:glx_Knowledge {id: 'k24'}) MERGE (k3)-[:PREREQUISITE]->(k24);",
                "MATCH (k24:glx_Knowledge {id: 'k24'}), (k25:glx_Knowledge {id: 'k25'}) MERGE (k24)-[:PREREQUISITE]->(k25);"
            ]
            execute_batch(session, "知识点前置关系创建（16-25）", batch10)
            time.sleep(1)
            
            # 第11批：创建知识点前置关系（26-30）和跨模块关系
            batch11 = [
                "MATCH (k24:glx_Knowledge {id: 'k24'}), (k26:glx_Knowledge {id: 'k26'}) MERGE (k24)-[:PREREQUISITE]->(k26);",
                "MATCH (k13:glx_Knowledge {id: 'k13'}), (k27:glx_Knowledge {id: 'k27'}) MERGE (k13)-[:PREREQUISITE]->(k27);",
                "MATCH (k27:glx_Knowledge {id: 'k27'}), (k28:glx_Knowledge {id: 'k28'}) MERGE (k27)-[:PREREQUISITE]->(k28);",
                "MATCH (k8:glx_Knowledge {id: 'k8'}), (k29:glx_Knowledge {id: 'k29'}) MERGE (k8)-[:PREREQUISITE]->(k29);",
                "MATCH (k29:glx_Knowledge {id: 'k29'}), (k30:glx_Knowledge {id: 'k30'}) MERGE (k29)-[:PREREQUISITE]->(k30);",
                "MATCH (k23:glx_Knowledge {id: 'k23'}), (k30:glx_Knowledge {id: 'k30'}) MERGE (k23)-[:PREREQUISITE]->(k30);"
            ]
            execute_batch(session, "知识点前置关系创建（26-30）及跨模块关系", batch11)
            
            # 验证导入结果
            print("\n" + "="*60)
            print("验证导入结果")
            print("="*60)
            
            result = session.run("MATCH (k:glx_Knowledge) RETURN count(k) as count")
            knowledge_count = result.single()["count"]
            print(f"✅ 知识点数量: {knowledge_count}")
            
            result = session.run("MATCH (m:glx_Module) RETURN count(m) as count")
            module_count = result.single()["count"]
            print(f"✅ 模块数量: {module_count}")
            
            result = session.run("MATCH (c:glx_Chapter) RETURN count(c) as count")
            chapter_count = result.single()["count"]
            print(f"✅ 章节数量: {chapter_count}")
            
            result = session.run("MATCH ()-[r]->() RETURN count(r) as count")
            relation_count = result.single()["count"]
            print(f"✅ 关系数量: {relation_count}")
            
            print("\n" + "="*60)
            print("✅ 数据导入完成!")
            print("="*60)
            
        driver.close()
        
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
