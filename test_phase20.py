#!/usr/bin/env python3
"""
阶段20测试：验证知识图谱可视化导出
"""
import sys
import os
import json

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from first_principles_agent import FirstPrincipleKG

print("=" * 60)
print("阶段20测试：知识图谱可视化导出")
print("=" * 60)

# 测试1：验证Graphviz导出
print("\n[测试1] 验证Graphviz DOT导出")
try:
    kg = FirstPrincipleKG()
    
    # 添加一些测试数据
    kg.add_node("测试节点1", {"type": "concept"})
    kg.add_node("测试节点2", {"type": "task"})
    kg.add_edge("测试节点1", "测试节点2", "关联", weight=0.8)
    
    # 导出
    dot_file = "test_kg_visualization.dot"
    success = kg.export_to_graphviz(dot_file)
    
    if success and os.path.exists(dot_file):
        print("✅ Graphviz DOT导出成功")
        with open(dot_file, "r", encoding="utf-8") as f:
            content = f.read()
        print(f"   文件大小: {len(content)} 字符")
        if "digraph KnowledgeGraph" in content:
            print("✅ DOT格式正确")
    else:
        print("❌ Graphviz DOT导出失败")
    
    # 清理
    if os.path.exists(dot_file):
        os.remove(dot_file)
        
except Exception as e:
    print(f"❌ Graphviz导出测试失败: {e}")
    import traceback
    traceback.print_exc()

# 测试2：验证JSON导出
print("\n[测试2] 验证JSON导出")
try:
    kg = FirstPrincipleKG()
    
    # 添加测试数据
    kg.add_node("JSON测试节点", {"type": "semantic"})
    
    # 导出
    json_file = "test_kg_export.json"
    success = kg.export_to_json(json_file)
    
    if success and os.path.exists(json_file):
        print("✅ JSON导出成功")
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        if "export_time" in data and "nodes" in data and "edges" in data:
            print("✅ JSON结构正确")
            print(f"   节点数: {len(data['nodes'])}")
            print(f"   边数: {len(data['edges'])}")
    else:
        print("❌ JSON导出失败")
    
    # 清理
    if os.path.exists(json_file):
        os.remove(json_file)
        
except Exception as e:
    print(f"❌ JSON导出测试失败: {e}")
    import traceback
    traceback.print_exc()

# 测试3：验证向后兼容
print("\n[测试3] 验证向后兼容")
try:
    kg = FirstPrincipleKG()
    # 验证基本功能不受影响
    kg.add_node("兼容测试")
    insights = kg.get_insights()
    print("✅ 向后兼容检查通过")
    print(f"   节点数: {insights['total_nodes']}")
except Exception as e:
    print(f"❌ 向后兼容测试失败: {e}")

print("\n" + "=" * 60)
print("阶段20测试完成！")
print("=" * 60)
