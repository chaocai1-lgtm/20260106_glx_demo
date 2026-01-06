"""
测试 Neo4j 连接
"""
from neo4j import GraphDatabase

# 连接配置
NEO4J_URI = "bolt://47.110.83.32:11001"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "mima123456"

try:
    print("正在连接 Neo4j...")
    print(f"URI: {NEO4J_URI}")
    print(f"Username: {NEO4J_USERNAME}")
    
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
    driver.verify_connectivity()
    
    print("✅ Neo4j 连接成功!")
    
    # 测试查询知识点数量
    with driver.session() as session:
        result = session.run("MATCH (k:glx_Knowledge) RETURN count(k) as count")
        count = result.single()['count']
        print(f"📊 知识点数量: {count}")
        
        # 查询模块信息
        result = session.run("MATCH (m:glx_Module) RETURN m.name as name, m.id as id")
        modules = [record.data() for record in result]
        print(f"📚 模块数量: {len(modules)}")
        for module in modules:
            print(f"  - {module['id']}: {module['name']}")
    
    driver.close()
    print("\n✅ 测试完成!")
    
except Exception as e:
    print(f"❌ 连接失败: {e}")
    import traceback
    traceback.print_exc()
