#!/usr/bin/env python3
"""
阶段21测试：验证插件系统接口
"""
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from first_principles_agent import PluginManager, FirstPrincipleEternalAgent

print("=" * 60)
print("阶段21测试：插件系统接口")
print("=" * 60)

# 测试1：验证PluginManager初始化
print("\n[测试1] 验证PluginManager初始化")
try:
    pm = PluginManager()
    print("✅ PluginManager初始化成功")
    print(f"   可用钩子: {list(pm.hooks.keys())}")
except Exception as e:
    print(f"❌ PluginManager初始化失败: {e}")

# 测试2：验证插件注册
print("\n[测试2] 验证插件注册")
try:
    pm = PluginManager()
    
    # 创建一个简单的测试插件
    class TestPlugin:
        def __init__(self):
            self.hooks = {
                "before_task": self.before_task,
                "after_task": self.after_task
            }
            self.before_count = 0
            self.after_count = 0
        
        def before_task(self, task):
            self.before_count += 1
            return f"before: {task}"
        
        def after_task(self, task):
            self.after_count += 1
            return f"after: {task}"
    
    plugin = TestPlugin()
    pm.register_plugin("test_plugin", plugin)
    
    print("✅ 插件注册成功")
    print(f"   已注册插件: {pm.list_plugins()}")
except Exception as e:
    print(f"❌ 插件注册测试失败: {e}")
    import traceback
    traceback.print_exc()

# 测试3：验证钩子执行
print("\n[测试3] 验证钩子执行")
try:
    # 执行before_task钩子
    results = pm.execute_hook("before_task", "测试任务")
    print(f"✅ 钩子执行成功")
    print(f"   结果: {results}")
    print(f"   before_count: {plugin.before_count}")
    
    # 执行after_task钩子
    results = pm.execute_hook("after_task", "测试任务")
    print(f"   after_count: {plugin.after_count}")
except Exception as e:
    print(f"❌ 钩子执行测试失败: {e}")
    import traceback
    traceback.print_exc()

# 测试4：验证插件注销
print("\n[测试4] 验证插件注销")
try:
    pm.unregister_plugin("test_plugin")
    print("✅ 插件注销成功")
    print(f"   剩余插件: {pm.list_plugins()}")
except Exception as e:
    print(f"❌ 插件注销测试失败: {e}")

# 测试5：验证Agent集成
print("\n[测试5] 验证Agent集成")
try:
    agent = FirstPrincipleEternalAgent()
    print("✅ Agent初始化成功（包含插件系统）")
    print(f"   插件管理器: {type(agent.plugin_manager).__name__}")
except Exception as e:
    print(f"❌ Agent集成测试失败: {e}")

print("\n" + "=" * 60)
print("阶段21测试完成！")
print("=" * 60)
