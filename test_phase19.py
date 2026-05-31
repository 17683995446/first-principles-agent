#!/usr/bin/env python3
"""
阶段19测试：验证任务优先级系统
"""
import sys
import os
from collections import deque

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 模拟TASK_POOL
import first_principles_agent
first_principles_agent.TASK_POOL = deque(maxlen=100)

from first_principles_agent import FirstPrincipleEternalAgent

print("=" * 60)
print("阶段19测试：任务优先级系统")
print("=" * 60)

# 测试1：验证优先级排序
print("\n[测试1] 验证优先级排序")
try:
    agent = FirstPrincipleEternalAgent()
    
    # 添加不同优先级的任务
    first_principles_agent.TASK_POOL.append("迭代_任务1")  # 低优先级
    first_principles_agent.TASK_POOL.append("普通任务")     # 普通优先级
    first_principles_agent.TASK_POOL.append("🎯 高优先级任务")  # 高优先级
    first_principles_agent.TASK_POOL.append("🔨 构建任务")     # 高优先级
    first_principles_agent.TASK_POOL.append("迭代_任务2")     # 低优先级
    
    print(f"   任务池大小: {len(first_principles_agent.TASK_POOL)}")
    
    # 获取任务，应该优先获取高优先级任务
    task1 = agent.get_task()
    print(f"   第一个任务: {task1}")
    
    task2 = agent.get_task()
    print(f"   第二个任务: {task2}")
    
    task3 = agent.get_task()
    print(f"   第三个任务: {task3}")
    
    # 验证优先级
    if "🎯" in task1 or "🔨" in task1:
        print("✅ 高优先级任务优先执行")
    else:
        print("❌ 高优先级任务未优先执行")
    
    if "迭代_" not in task3:
        print("✅ 迭代任务被推迟执行")
    else:
        print("⚠️ 迭代任务可能过早执行")
        
except Exception as e:
    print(f"❌ 优先级排序测试失败: {e}")
    import traceback
    traceback.print_exc()

# 测试2：验证空任务池
print("\n[测试2] 验证空任务池")
try:
    agent = FirstPrincipleEternalAgent()
    first_principles_agent.TASK_POOL.clear()
    
    task = agent.get_task()
    if task is None:
        print("✅ 空任务池处理正确")
    else:
        print(f"❌ 空任务池返回非None: {task}")
except Exception as e:
    print(f"❌ 空任务池测试失败: {e}")

# 测试3：验证向后兼容
print("\n[测试3] 验证向后兼容")
try:
    first_principles_agent.TASK_POOL.append("普通任务1")
    first_principles_agent.TASK_POOL.append("普通任务2")
    
    agent = FirstPrincipleEternalAgent()
    task = agent.get_task()
    
    if task in ["普通任务1", "普通任务2"]:
        print("✅ 向后兼容检查通过")
    else:
        print(f"❌ 向后兼容问题: {task}")
except Exception as e:
    print(f"❌ 向后兼容测试失败: {e}")

print("\n" + "=" * 60)
print("阶段19测试完成！")
print("=" * 60)
