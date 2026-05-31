#!/usr/bin/env python3
"""
阶段15测试：验证快速测试模式
"""
import sys
import os
import subprocess
import time

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("阶段15测试：快速测试模式")
print("=" * 60)

# 测试1：验证帮助信息包含 --quick-test
print("\n[测试1] 验证帮助信息包含 --quick-test")
try:
    result = subprocess.run(
        [sys.executable, "first_principles_agent.py", "--help"],
        capture_output=True,
        text=True,
        timeout=5
    )
    if "--quick-test" in result.stdout:
        print("✅ 帮助信息包含 --quick-test")
    else:
        print("❌ 帮助信息不包含 --quick-test")
except Exception as e:
    print(f"⚠️  帮助信息测试: {e}")

# 测试2：快速测试模式 - 运行3轮
print("\n[测试2] 验证快速测试模式（3轮")
try:
    start_time = time.time()
    # 使用 --no-llm 和 --quick-test=3 来快速测试
    result = subprocess.run(
        [sys.executable, "first_principles_agent.py", "--no-llm", "--quick-test=3", "--loop-sleep=0.1"],
        capture_output=True,
        text=True,
        timeout=30
    )
    elapsed = time.time() - start_time
    
    if result.returncode == 0:
        print(f"✅ 快速测试模式运行成功，耗时 {elapsed:.1f} 秒")
        # 检查输出
        if "快速测试完成" in result.stdout:
            print("✅ 输出包含快速测试完成信息")
        if "总运行 3 轮" in result.stdout:
            print("✅ 输出包含运行3轮信息")
    else:
        print(f"❌ 快速测试模式失败，返回码: {result.returncode}")
        print(f"   stdout: {result.stdout[:200]}")
except Exception as e:
    print(f"⚠️  快速测试模式测试: {e}")

# 测试3：验证正常模式（向后兼容）
print("\n[测试3] 验证向后兼容性")
try:
    from first_principles_agent import FirstPrincipleEternalAgent, Config
    # 验证不传递 quick_test 参数初始化
    agent = FirstPrincipleEternalAgent()
    print("✅ Agent初始化成功（向后兼容）")
    print(f"   - quick_test_rounds: {agent.quick_test_rounds}")
except Exception as e:
    print(f"❌ 向后兼容测试失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("阶段15测试完成！")
print("=" * 60)
