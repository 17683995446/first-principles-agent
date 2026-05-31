#!/usr/bin/env python3
"""
阶段26测试：验证API接口封装
"""
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from first_principles_agent import APIWrapper, FirstPrincipleEternalAgent

print("=" * 60)
print("阶段26测试：API接口封装")
print("=" * 60)

# 测试1：验证APIWrapper初始化
print("\n[测试1] 验证APIWrapper初始化")
try:
    agent = FirstPrincipleEternalAgent()
    api = APIWrapper(agent)
    print("✅ APIWrapper初始化成功")
    print(f"   路由数: GET={len(api.routes['GET'])}, POST={len(api.routes['POST'])}")
except Exception as e:
    print(f"❌ APIWrapper初始化失败: {e}")

# 测试2：验证状态接口
print("\n[测试2] 验证状态接口")
try:
    result = api.handle_request("GET", "/status")
    if result.get("status") == 200:
        print("✅ 状态接口正常")
        print(f"   run_count: {result.get('run_count')}")
        print(f"   alive: {result.get('alive')}")
    else:
        print(f"❌ 状态接口异常: {result}")
except Exception as e:
    print(f"❌ 状态接口测试失败: {e}")

# 测试3：验证洞察接口
print("\n[测试3] 验证洞察接口")
try:
    result = api.handle_request("GET", "/insights")
    if result.get("status") == 200:
        print("✅ 洞察接口正常")
        print(f"   节点数: {result.get('total_nodes')}")
        print(f"   边数: {result.get('total_edges')}")
    else:
        print(f"❌ 洞察接口异常: {result}")
except Exception as e:
    print(f"❌ 洞察接口测试失败: {e}")

# 测试4：验证任务接口
print("\n[测试4] 验证任务接口")
try:
    # 添加任务
    result = api.handle_request("POST", "/tasks", {"task": "API测试任务"})
    if result.get("status") == 200:
        print("✅ 添加任务接口正常")
    else:
        print(f"❌ 添加任务接口异常: {result}")
    
    # 获取任务列表
    result = api.handle_request("GET", "/tasks")
    if result.get("status") == 200:
        print("✅ 获取任务接口正常")
        print(f"   任务数: {result.get('task_count')}")
    else:
        print(f"❌ 获取任务接口异常: {result}")
except Exception as e:
    print(f"❌ 任务接口测试失败: {e}")

# 测试5：验证配置接口
print("\n[测试5] 验证配置接口")
try:
    result = api.handle_request("GET", "/config")
    if result.get("status") == 200:
        print("✅ 配置接口正常")
        config = result.get("config", {})
        print(f"   LOOP_SLEEP: {config.get('LOOP_SLEEP')}")
    else:
        print(f"❌ 配置接口异常: {result}")
except Exception as e:
    print(f"❌ 配置接口测试失败: {e}")

# 测试6：验证404处理
print("\n[测试6] 验证404处理")
try:
    result = api.handle_request("GET", "/notfound")
    if result.get("status") == 404:
        print("✅ 404处理正常")
    else:
        print(f"❌ 404处理异常: {result}")
except Exception as e:
    print(f"❌ 404测试失败: {e}")

# 测试7：验证Agent集成
print("\n[测试7] 验证Agent集成")
try:
    agent = FirstPrincipleEternalAgent()
    print("✅ Agent集成API成功")
    print(f"   api类型: {type(agent.api).__name__}")
except Exception as e:
    print(f"❌ Agent集成测试失败: {e}")

print("\n" + "=" * 60)
print("阶段26测试完成！")
print("=" * 60)
