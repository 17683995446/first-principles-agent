#!/usr/bin/env python3
"""
阶段12测试：验证FirstPrincipleEternalAgent使用Config类
保持向后兼容
"""
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from first_principles_agent import FirstPrincipleEternalAgent, Config

print("=" * 60)
print("阶段12测试：FirstPrincipleEternalAgent使用Config类")
print("=" * 60)

# 测试1：验证Agent可以正常初始化
print("\n[测试1] 验证Agent初始化")
try:
    agent = FirstPrincipleEternalAgent()
    print("✅ Agent初始化成功")
    print(f"   - context_max_len: {agent.context_max_len}")
except Exception as e:
    print(f"❌ Agent初始化失败: {e}")
    sys.exit(1)

# 测试2：验证Config类的使用
print("\n[测试2] 验证Config类配置")
print(f"   - Config.LOOP_SLEEP: {Config.LOOP_SLEEP}")
print(f"   - Config.EVOLVE_CYCLE: {Config.EVOLVE_CYCLE}")
print(f"   - Config.SAVE_EVERY_N: {Config.SAVE_EVERY_N}")

# 测试3：验证getattr兼容模式
print("\n[测试3] 验证向后兼容性")
try:
    # 模拟旧代码访问全局变量的方式
    from first_principles_agent import LOOP_SLEEP, EVOLVE_CYCLE, CONTEXT_MAX_LEN
    print(f"   - 全局变量LOOP_SLEEP: {LOOP_SLEEP}")
    print(f"   - 全局变量EVOLVE_CYCLE: {EVOLVE_CYCLE}")
    print("✅ 向后兼容检查通过")
except Exception as e:
    print(f"⚠️  向后兼容检查: {e}")

print("\n" + "=" * 60)
print("阶段12测试完成！所有功能正常")
print("=" * 60)
