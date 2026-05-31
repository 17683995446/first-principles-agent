#!/usr/bin/env python3
"""
阶段25测试：验证代码重构和优化
"""
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from first_principles_agent import (
    FirstPrincipleEternalAgent, 
    FirstPrincipleKG,
    Config,
    Logger,
    PerformanceMonitor,
    PluginManager,
    I18n
)

print("=" * 60)
print("阶段25测试：代码重构和优化")
print("=" * 60)

# 测试1：验证版本号更新
print("\n[测试1] 验证版本号更新")
try:
    # 检查文件中的版本号
    with open("first_principles_agent.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    if "2.4.0" in content:
        print("✅ 版本号已更新到 2.4.0")
    else:
        print("❌ 版本号未更新")
except Exception as e:
    print(f"❌ 版本号检查失败: {e}")

# 测试2：验证所有新组件可导入
print("\n[测试2] 验证所有新组件可导入")
try:
    components = [
        ("Config", Config),
        ("Logger", Logger),
        ("PerformanceMonitor", PerformanceMonitor),
        ("PluginManager", PluginManager),
        ("I18n", I18n),
        ("FirstPrincipleKG", FirstPrincipleKG),
        ("FirstPrincipleEternalAgent", FirstPrincipleEternalAgent)
    ]
    
    for name, cls in components:
        print(f"   ✅ {name}")
    
    print("✅ 所有组件可正常导入")
except Exception as e:
    print(f"❌ 组件导入失败: {e}")

# 测试3：验证Agent集成所有新功能
print("\n[测试3] 验证Agent集成所有新功能")
try:
    agent = FirstPrincipleEternalAgent()
    
    checks = {
        "i18n": hasattr(agent, 'i18n') and agent.i18n is not None,
        "perf_monitor": hasattr(agent, 'perf_monitor') and agent.perf_monitor is not None,
        "plugin_manager": hasattr(agent, 'plugin_manager') and agent.plugin_manager is not None
    }
    
    all_ok = True
    for name, result in checks.items():
        if result:
            print(f"   ✅ {name}")
        else:
            print(f"   ❌ {name}")
            all_ok = False
    
    if all_ok:
        print("✅ Agent集成所有新功能")
    else:
        print("❌ Agent部分功能未集成")
except Exception as e:
    print(f"❌ Agent集成测试失败: {e}")
    import traceback
    traceback.print_exc()

# 测试4：验证向后兼容
print("\n[测试4] 验证向后兼容")
try:
    agent = FirstPrincipleEternalAgent()
    
    # 测试基本功能
    agent.kg.add_node("兼容测试")
    insights = agent.kg.get_insights()
    
    # 测试配置
    config_value = getattr(Config, 'LOOP_SLEEP', None)
    
    if insights and config_value is not None:
        print("✅ 向后兼容检查通过")
        print(f"   节点数: {insights['total_nodes']}")
        print(f"   LOOP_SLEEP: {config_value}")
    else:
        print("❌ 向后兼容问题")
except Exception as e:
    print(f"❌ 向后兼容测试失败: {e}")

# 测试5：验证代码结构完整性
print("\n[测试5] 验证代码结构完整性")
try:
    with open("first_principles_agent.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    required_components = [
        "class Config",
        "class Logger",
        "class PerformanceMonitor",
        "class PluginManager",
        "class I18n",
        "class FirstPrincipleKG",
        "class FirstPrincipleEternalAgent"
    ]
    
    all_found = True
    for component in required_components:
        if component in content:
            print(f"   ✅ {component}")
        else:
            print(f"   ❌ {component} 未找到")
            all_found = False
    
    if all_found:
        print("✅ 代码结构完整")
    else:
        print("❌ 代码结构不完整")
except Exception as e:
    print(f"❌ 代码结构检查失败: {e}")

print("\n" + "=" * 60)
print("阶段25测试完成！")
print("=" * 60)
