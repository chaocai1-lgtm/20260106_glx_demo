"""
导入管理学知识图谱数据到 Neo4j
"""
from neo4j import GraphDatabase
import os

# 连接配置
NEO4J_URI = "bolt://47.110.83.32:11001"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "mima123456"

# 获取脚本路径
script_dir = os.path.dirname(os.path.abspath(__file__))
cypher_file = os.path.join(script_dir, "data", "init_management_data.cypher")

try:
    print("正在连接 Neo4j...")
    print(f"URI: {NEO4J_URI}")
    driver = GraphDatabase.driver(
        NEO4J_URI, 
        auth=(NEO4J_USERNAME, NEO4J_PASSWORD),
        connection_timeout=30,
        max_connection_lifetime=300
    )
    driver.verify_connectivity()
    print("✅ Neo4j 连接成功!")
    
    print(f"\n正在读取 Cypher 脚本: {cypher_file}")
    with open(cypher_file, 'r', encoding='utf-8') as f:
        cypher_script = f.read()
    
    # 分割成多个语句（以分号分隔）
    statements = [s.strip() for s in cypher_script.split(';') if s.strip() and not s.strip().startswith('//')]
    
    print(f"找到 {len(statements)} 条语句")
    
    with driver.session() as session:
        for i, statement in enumerate(statements, 1):
            if statement:
                print(f"执行语句 {i}/{len(statements)}...", end='\r')
                try:
                    session.run(statement)
                except Exception as e:
                    print(f"\n⚠️ 语句 {i} 执行失败: {e}")
                    print(f"语句内容: {statement[:100]}...")
    
    print(f"\n✅ 数据导入完成!")
    
    # 验证数据
    print("\n验证导入的数据:")
    with driver.session() as session:
        # 检查模块
        result = session.run("MATCH (m:glx_Module) RETURN count(m) as count")
        module_count = result.single()['count']
        print(f"📚 模块数量: {module_count}")
        
        # 检查章节
        result = session.run("MATCH (c:glx_Chapter) RETURN count(c) as count")
        chapter_count = result.single()['count']
        print(f"📖 章节数量: {chapter_count}")
        
        # 检查知识点
        result = session.run("MATCH (k:glx_Knowledge) RETURN count(k) as count")
        knowledge_count = result.single()['count']
        print(f"📝 知识点数量: {knowledge_count}")
        
        # 检查关系
        result = session.run("MATCH ()-[r:CONTAINS]->() RETURN count(r) as count")
        contains_count = result.single()['count']
        print(f"🔗 CONTAINS 关系数量: {contains_count}")
        
        result = session.run("MATCH ()-[r:PREREQUISITE]->() RETURN count(r) as count")
        prereq_count = result.single()['count']
        print(f"🔗 PREREQUISITE 关系数量: {prereq_count}")
        
        # 显示模块信息
        print("\n📚 模块列表:")
        result = session.run("MATCH (m:glx_Module) RETURN m.id as id, m.name as name ORDER BY m.id")
        for record in result:
            print(f"  {record['id']}: {record['name']}")
    
    driver.close()
    print("\n✅ 全部完成!")
    
except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback
    traceback.print_exc()
