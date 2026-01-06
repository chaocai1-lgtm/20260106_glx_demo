"""
案例库模块（管理学）
提供管理学案例浏览、搜索和详情查看功能
"""

import streamlit as st

# 可选导入Elasticsearch（仅本地开发需要）
try:
    from elasticsearch import Elasticsearch
    HAS_ELASTICSEARCH = True
except ImportError:
    HAS_ELASTICSEARCH = False
    Elasticsearch = None

try:
    from config.settings import ELASTICSEARCH_CLOUD_ID, ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD
except (ImportError, AttributeError):
    ELASTICSEARCH_CLOUD_ID = None
    ELASTICSEARCH_USERNAME = None
    ELASTICSEARCH_PASSWORD = None

def ensure_list(value, default=None):
    """确保值是列表格式，如果是字符串则分割"""
    if default is None:
        default = []
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        # 如果是字符串，按换行符分割
        return [line.strip() for line in value.split('\n') if line.strip()]
    return default

def check_neo4j_available():
    """检查Neo4j是否可用"""
    from modules.auth import check_neo4j_available as auth_check
    return auth_check()

def get_neo4j_driver():
    """获取Neo4j连接（复用auth模块的缓存连接）"""
    from modules.auth import get_neo4j_driver as auth_get_driver
    return auth_get_driver()

def get_current_student():
    """获取当前学生信息"""
    if st.session_state.get('user_role') == 'student':
        return st.session_state.get('student_id')
    return None

def log_case_activity(activity_type, case_id=None, case_title=None, details=None):
    """记录案例库活动"""
    student_id = get_current_student()
    if not student_id:
        return
    
    from modules.auth import log_activity
    log_activity(
        student_id=student_id,
        activity_type=activity_type,
        module_name="案例库",
        content_id=case_id,
        content_name=case_title,
        details=details
    )

def search_cases(query="", difficulty=None):
    """搜索病例（仅本地开发可用，云端返回None）"""
    # 云端部署时跳过Elasticsearch
    if not HAS_ELASTICSEARCH or not ELASTICSEARCH_CLOUD_ID:
        return None
    
    try:
        es = Elasticsearch(
            cloud_id=ELASTICSEARCH_CLOUD_ID,
            basic_auth=(ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD)
        )
        
        # 构建搜索查询
        if query:
            search_body = {
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["title", "symptoms", "diagnosis", "chief_complaint"]
                    }
                }
            }
        else:
            search_body = {"query": {"match_all": {}}}
        
        # 添加难度过滤
        if difficulty:
            search_body["query"] = {
                "bool": {
                    "must": [search_body["query"]],
                    "filter": [{"term": {"difficulty": difficulty}}]
                }
            }
        
        result = es.search(index="mfx_cases", body=search_body, size=10)
        es.close()
        
        return [hit["_source"] for hit in result["hits"]["hits"]]
    except Exception:
        return []

def get_case_detail(case_id):
    """从Neo4j获取病例详情"""
    if not check_neo4j_available():
        return None
    
    try:
        driver = get_neo4j_driver()
        
        with driver.session() as session:
            # 获取病例基本信息
            result = session.run("""
                MATCH (c:mfx_Case {id: $case_id})
                RETURN c
            """, case_id=case_id)
            
            case = result.single()
            if not case:
                return None
            
            case_data = dict(case['c'])
            
            # 获取关联的知识点
            result = session.run("""
                MATCH (c:mfx_Case {id: $case_id})-[:RELATES_TO]->(k:mfx_Knowledge)
                RETURN k.id as id, k.name as name
            """, case_id=case_id)
            
            case_data['knowledge_points'] = [dict(record) for record in result]
        
        return case_data
    except Exception:
        return None


def adapt_case_for_display(case):
    """将管理学案例数据转换为显示格式"""
    # 如果已经是标准格式，直接返回
    if "diagnosis" in case and "chief_complaint" in case:
        return case
    
    # 新格式案例需要转换
    adapted = case.copy()
    
    # 基本信息
    adapted["title"] = case.get("title", "未命名案例")
    adapted["difficulty"] = case.get("difficulty", "中等")
    
    # 核心字段映射
    adapted["chief_complaint"] = case.get("case_info", "")  # 案例背景
    adapted["diagnosis"] = f"{case.get('category', '')} - {case.get('subcategory', '')}"  # 分类
    adapted["symptoms"] = case.get("keywords", [])  # 关键词
    
    # 分析内容结构
    adapted["diagnosis_analysis"] = {
        "clinical_exam": {
            "title": "案例背景",
            "items": [case.get("case_info", "")]
        },
        "radiographic": {
            "title": "案例分析",
            "items": [case.get("court_opinion", "")]
        },
        "differential": {
            "title": "相关知识",
            "items": case.get("related_knowledge", [])
        }
    }
    
    # 讨论问题
    adapted["questions"] = case.get("questions", [])
    
    return adapted


@st.cache_data(ttl=3600, show_spinner=False)
def get_all_sample_cases():
    """从data/cases.py获取管理学案例"""
    try:
        from data.cases import get_cases
        cases = get_cases()
        # 转换格式
        adapted_cases = [adapt_case_for_display(case) for case in cases]
        return adapted_cases
    except Exception as e:
        st.error(f"加载案例失败: {str(e)}")
        return []

def render_case_library():
    """渲染管理学案例库页面"""
    st.title("📚 管理学案例学习中心")
    
    # 初始化session_state以减少刷新
    if 'case_library_initialized' not in st.session_state:
        st.session_state.case_library_initialized = True
        st.session_state.selected_case_index = 0
    
    # 记录进入案例库（只记录一次）
    if 'case_activity_logged' not in st.session_state:
        log_case_activity("进入模块", details="访问案例库")
        st.session_state.case_activity_logged = True
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px;">
        <h3 style="margin: 0; color: white;">📚 管理学案例库</h3>
        <p style="margin: 10px 0 0 0; opacity: 0.9; color: white;">通过真实管理案例学习，掌握管理理论与实践的核心技能</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 获取所有案例供选择（使用缓存数据）
    all_cases = get_all_sample_cases()
    
    # 案例选择区
    st.markdown("### 📂 选择学习案例")
    
    case_options = {f"📊 {c['title']}": c for c in all_cases}
    selected_case_name = st.selectbox(
        "选择案例进行学习",
        options=list(case_options.keys()),
        index=0,
        label_visibility="collapsed",
        help="从下拉列表中选择一个病例进行深入学习"
    )
    
    selected_case = case_options.get(selected_case_name)
    
    if selected_case:
        # 记录查看病例
        log_case_activity("查看病例", case_id=selected_case['id'], case_title=selected_case['title'])
        
        st.divider()
        
        # 病例头部信息卡片
        difficulty_colors = {"简单": "#28a745", "中等": "#ffc107", "困难": "#dc3545"}
        diff_color = difficulty_colors.get(selected_case['difficulty'], "#6c757d")
        
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid {diff_color};">
            <h2 style="margin: 0 0 10px 0;">📋 {selected_case['title']}</h2>
            <div style="display: flex; gap: 20px; flex-wrap: wrap;">
                <span style="background: {diff_color}; color: white; padding: 5px 15px; border-radius: 20px;">
                    难度: {selected_case['difficulty']}
                </span>
                <span style="background: #17a2b8; color: white; padding: 5px 15px; border-radius: 20px;">
                    分类: {selected_case['diagnosis']}
                </span>
                <span style="background: #6c757d; color: white; padding: 5px 15px; border-radius: 20px;">
                    ID: {selected_case['id']}
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("")
        
        # 案例信息（如果有）
        if 'patient_info' in selected_case:
            patient = selected_case['patient_info']
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"**🏢 企业规模：** {patient.get('age', '-')}")
            with col2:
                st.markdown(f"**🏭 行业类型：** {patient.get('gender', '-')}")
            with col3:
                st.markdown(f"**📍 所在地区：** {patient.get('occupation', '-')}")
            with col4:
                st.markdown(f"**📋 案例编号：** {selected_case['id']}")
        
        # 使用选项卡组织内容
        tab1, tab2, tab3, tab4 = st.tabs(["📋 案例背景", "🔍 管理分析", "💡 解决方案", "📝 学习要点"])
        
        with tab1:
            # 案例概述
            st.markdown("#### 📢 案例概述")
            st.info(selected_case['chief_complaint'])
            
            # 案例情境
            if 'present_illness' in selected_case:
                st.markdown("#### 📖 案例情境")
                st.markdown(f'<div style="background: #fff3e0; padding: 15px; border-radius: 8px; border-left: 4px solid #ff9800; white-space: pre-line;">{selected_case["present_illness"]}</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 📋 企业背景")
                medical_history = selected_case.get('medical_history', '企业基本情况良好，处于正常运营状态')
                st.markdown(f'<div style="background: #fce4ec; padding: 15px; border-radius: 8px; border-left: 4px solid #e91e63; white-space: pre-line;">{medical_history}</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown("#### 🔍 关键问题")
                symptoms = selected_case['symptoms']
                if isinstance(symptoms, list):
                    for s in symptoms:
                        st.markdown(f'<div style="background: #e3f2fd; padding: 8px 12px; margin: 4px 0; border-radius: 5px; border-left: 3px solid #2196f3;">• {s}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(symptoms)
            
            # 管理挑战（新增）
            if 'clinical_manifestation' in selected_case:
                st.markdown("#### 🎯 管理挑战")
                st.markdown(f'<div style="background: #f3e5f5; padding: 15px; border-radius: 8px; border-left: 4px solid #9c27b0; white-space: pre-line;">{selected_case["clinical_manifestation"]}</div>', unsafe_allow_html=True)
            
            # 数据与分析（新增）
            if 'auxiliary_examination' in selected_case:
                st.markdown("#### 📊 数据与分析")
                st.markdown(f'<div style="background: #e8f5e9; padding: 15px; border-radius: 8px; border-left: 4px solid #4caf50; white-space: pre-line;">{selected_case["auxiliary_examination"]}</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown("#### 🔍 管理分析")
            st.success(f"**{selected_case['diagnosis']}**")
            
            # 管理检查结果
            if 'examination' in selected_case:
                st.markdown("#### 📊 管理诊断")
                examination = selected_case['examination']
                
                # 创建两列布局
                col1, col2 = st.columns(2)
                
                with col1:
                    if 'organizational_structure' in examination:
                        st.markdown(f'<div style="background: #e8f5e9; padding: 10px; margin: 5px 0; border-radius: 5px; border-left: 3px solid #4caf50;"><strong>🏢 组织结构：</strong>{examination["organizational_structure"]}</div>', unsafe_allow_html=True)
                    if 'management_system' in examination:
                        st.markdown(f'<div style="background: #e3f2fd; padding: 10px; margin: 5px 0; border-radius: 5px; border-left: 3px solid #2196f3;"><strong>📋 管理制度：</strong>{examination["management_system"]}</div>', unsafe_allow_html=True)
                    if 'financial_control' in examination:
                        st.markdown(f'<div style="background: #fff3e0; padding: 10px; margin: 5px 0; border-radius: 5px; border-left: 3px solid #ff9800;"><strong>💰 财务管控：</strong>{examination["financial_control"]}</div>', unsafe_allow_html=True)
                
                with col2:
                    if 'hr_system' in examination:
                        st.markdown(f'<div style="background: #fce4ec; padding: 10px; margin: 5px 0; border-radius: 5px; border-left: 3px solid #e91e63;"><strong>👥 人力资源：</strong>{examination["hr_system"]}</div>', unsafe_allow_html=True)
                    if 'decision_making' in examination:
                        st.markdown(f'<div style="background: #f3e5f5; padding: 10px; margin: 5px 0; border-radius: 5px; border-left: 3px solid #9c27b0;"><strong>⚖️ 决策机制：</strong>{examination["decision_making"]}</div>', unsafe_allow_html=True)
                    if 'technology_level' in examination:
                        st.markdown(f'<div style="background: #e0f2f1; padding: 10px; margin: 5px 0; border-radius: 5px; border-left: 3px solid #009688;"><strong>🔧 技术水平：</strong>{examination["technology_level"]}</div>', unsafe_allow_html=True)
            
            # 阶段与严重度分析
            if 'stage_grade_analysis' in selected_case:
                st.markdown("")
                st.markdown("#### 📈 问题分析")
                stage_analysis = selected_case['stage_grade_analysis']
                
                col1, col2 = st.columns(2)
                with col1:
                    if 'stage' in stage_analysis:
                        st.markdown(f'<div style="background: #e1f5fe; padding: 12px; border-radius: 8px; border-left: 4px solid #0288d1;"><strong>📊 发展阶段：</strong><br>{stage_analysis["stage"]}</div>', unsafe_allow_html=True)
                with col2:
                    if 'grade' in stage_analysis:
                        st.markdown(f'<div style="background: #fff9c4; padding: 12px; border-radius: 8px; border-left: 4px solid #fbc02d;"><strong>⚠️ 严重程度：</strong><br>{stage_analysis["grade"]}</div>', unsafe_allow_html=True)
            
            # 管理要点
            st.markdown("")
            st.markdown("#### 💡 管理要点")
            key_points = ensure_list(
                selected_case.get('key_points'),
                ['识别核心问题', '分析关键因素', '制定解决方案']
            )
            for i, point in enumerate(key_points, 1):
                st.markdown(f'<div style="background: #e7f3ff; padding: 12px; margin: 8px 0; border-radius: 8px; border-left: 4px solid #0066cc;"><strong>{i}.</strong> {point}</div>', unsafe_allow_html=True)
        
        with tab3:
            st.markdown("#### � 解决方案")
            treatment = ensure_list(
                selected_case.get('treatment_plan'), 
                ['问题诊断', '方案设计', '实施建议']
            )
            
            current_phase = None
            step_count = 0
            
            for step in treatment:
                # 检测是否是阶段标题（包含【】）
                if step.startswith('【') and '】' in step:
                    current_phase = step
                    st.markdown(f'<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px 20px; margin: 15px 0 10px 0; border-radius: 8px;"><strong>{step}</strong></div>', unsafe_allow_html=True)
                else:
                    step_count += 1
                    st.markdown(f'<div style="background: #f5f5f5; padding: 12px 15px; margin: 5px 0 5px 20px; border-radius: 8px; border-left: 4px solid #4ECDC4;">{step}</div>', unsafe_allow_html=True)
            
            # 实施建议（新增字段）
            if 'treatment_notes' in selected_case:
                st.markdown("#### ⚠️ 实施建议")
                st.markdown(f'<div style="background: #fff8e1; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #ffc107; white-space: pre-line;">{selected_case["treatment_notes"]}</div>', unsafe_allow_html=True)
        
        with tab4:
            st.markdown("#### 📝 学习要点总结")
            
            # 显示关键学习要点
            key_points = ensure_list(
                selected_case.get('key_points'),
                ['理解案例背景', '分析管理问题', '掌握解决思路']
            )
            for i, point in enumerate(key_points, 1):
                st.markdown(f'<div style="background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); padding: 12px 15px; margin: 8px 0; border-radius: 8px; border-left: 4px solid #4caf50;"><strong>要点 {i}：</strong> {point}</div>', unsafe_allow_html=True)
            
            st.markdown("")
            st.markdown("#### ✏️ 我的学习笔记")
            notes = st.text_area(
                "记录你对这个案例的理解、疑问和思考",
                height=150,
                placeholder="例如：\n1. 这个案例的管理问题是...\n2. 解决方案的关键点是...\n3. 需要进一步学习的内容...",
                key=f"notes_{selected_case['id']}"
            )
            
            col1, col2 = st.columns([1, 3])
            with col1:
                if st.button("💾 保存笔记", type="primary", key=f"save_notes_{selected_case['id']}"):
                    if notes:
                        log_case_activity("保存笔记", case_id=selected_case['id'], 
                                        case_title=selected_case['title'], 
                                        details=f"笔记: {notes[:100]}")
                        st.success("✅ 笔记已保存！")
                    else:
                        st.warning("请先输入笔记内容")
            with col2:
                st.markdown("*笔记将保存到你的学习记录中*")
