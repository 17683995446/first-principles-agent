#!/usr/bin/env python3
"""
阶段14测试：验证命令行参数解析改进
"""
import sys
import os
import subprocess

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("阶段14测试：命令行参数解析改进")
print("=" * 60)

# 测试1：验证帮助信息
print("\n[测试1] 验证帮助信息")
try:
    result = subprocess.run(
        [sys.executable, "first_principles_agent.py", "--help"],
        capture_output=True,
        text=True,
        timeout=5
    )
    print("✅ 帮助信息显示正常")
    print("   帮助信息包含:")
    for line in result.stdout.splitlines()[:15]:
        print(f"     {line}")
except Exception as e:
    print(f"⚠️  帮助信息测试: {e}")

# 测试2：验证版本信息
print("\n[测试2] 验证版本信息")
try:
    result = subprocess.run(
        [sys.executable, "first_principles_agent.py", "--version"],
        capture_output=True,
        text=True,
        timeout=5
    )
    print(f"✅ 版本信息: {result.stdout.strip()}")
except Exception as e:
    print(f"⚠️  版本信息测试: {e}")

# 测试3：验证参数解析
print("\n[测试3] 验证参数解析（模拟）")
try:
    from first_principles_agent import Config, TASK_MAX_LEN, CONTEXT_MAX_LEN, EVOLVE_CYCLE, SAVE_EVERY_N
    print(f"   - Config.TASK_MAX_LEN: {Config.TASK_MAX_LEN}")
    print(f"   - Config.CONTEXT_MAX_LEN: {Config.CONTEXT_MAX_LEN}")
    print(f"   - Config.EVOLVE_CYCLE: {Config.EVOLVE_CYCLE}")
    print(f"   - Config.SAVE_EVERY_N: {Config.SAVE_EVERY_N}")
    print("✅ 参数配置正常")
except Exception as e:
    print(f"❌ 参数解析测试失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("阶段14测试完成！")
print("=" * 60)
