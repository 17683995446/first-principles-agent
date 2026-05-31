#!/usr/bin/env python3
"""
阶段27测试：验证任务调度器（TaskScheduler类）
"""
import sys
import os
import time

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from first_principles_agent import TaskScheduler, FirstPrincipleEternalAgent

print("=" * 60)
print("阶段27测试：任务调度器（TaskScheduler类）")
print("=" * 60)

# 测试1：验证TaskScheduler初始化
print("\n[测试1] 验证TaskScheduler初始化")
try:
    scheduler = TaskScheduler()
    assert scheduler.get_task_count() == 0
    print("✅ TaskScheduler初始化成功")
    print(f"   任务数: {scheduler.get_task_count()}")
except Exception as e:
    print(f"❌ TaskScheduler初始化失败: {e}")

# 测试2：验证定时任务调度
print("\n[测试2] 验证定时任务调度")
try:
    scheduler = TaskScheduler()
    result_holder = {"executed": False}

    def test_func():
        result_holder["executed"] = True
        return "done"

    task_id = scheduler.schedule_once(test_func, time.time() + 0.1, priority=3)
    assert task_id is not None
    assert scheduler.get_task_count() == 1
    print(f"✅ 定时任务调度成功，任务ID: {task_id}")
except Exception as e:
    print(f"❌ 定时任务调度失败: {e}")

# 测试3：验证周期性任务调度
print("\n[测试3] 验证周期性任务调度")
try:
    scheduler = TaskScheduler()

    def periodic_func():
        return "periodic"

    task_id = scheduler.schedule_periodic(periodic_func, interval=0.2, priority=2)
    assert task_id is not None
    assert scheduler.get_task_count() == 1
    print(f"✅ 周期性任务调度成功，任务ID: {task_id}")
except Exception as e:
    print(f"❌ 周期性任务调度失败: {e}")

# 测试4：验证任务优先级排序
print("\n[测试4] 验证任务优先级排序")
try:
    scheduler = TaskScheduler()
    results = []

    def low_priority():
        results.append("low")
        return "low"

    def high_priority():
        results.append("high")
        return "high"

    scheduler.schedule_once(low_priority, time.time(), priority=9)
    scheduler.schedule_once(high_priority, time.time(), priority=1)

    pending = scheduler.get_pending_tasks()
    assert len(pending) == 2
    assert pending[0]["priority"] < pending[1]["priority"]
    print("✅ 任务优先级排序正确")
    print(f"   优先级顺序: {pending[0]['priority']} < {pending[1]['priority']}")
except Exception as e:
    print(f"❌ 任务优先级排序失败: {e}")

# 测试5：验证任务执行
print("\n[测试5] 验证任务执行")
try:
    scheduler = TaskScheduler()
    exec_result = {"value": None}

    def exec_func(arg1, arg2):
        exec_result["value"] = arg1 + arg2
        return exec_result["value"]

    task_id = scheduler.schedule_once(exec_func, time.time(), priority=5, args=(10, 20))
    result = scheduler.execute_task(task_id)
    assert result["success"] is True
    assert result["result"] == 30
    assert exec_result["value"] == 30
    print("✅ 任务执行成功")
    print(f"   执行结果: {result['result']}")
except Exception as e:
    print(f"❌ 任务执行失败: {e}")

# 测试6：验证周期性任务执行和重复触发
print("\n[测试6] 验证周期性任务执行和重复触发")
try:
    scheduler = TaskScheduler()
    counter = {"count": 0}

    def count_func():
        counter["count"] += 1
        return counter["count"]

    task_id = scheduler.schedule_periodic(count_func, interval=0.05, priority=5)
    time.sleep(0.12)
    due = scheduler.get_due_periodic_tasks()
    assert len(due) >= 1
    scheduler.run_due_tasks()
    time.sleep(0.08)
    scheduler.run_due_tasks()
    assert counter["count"] >= 2
    print(f"✅ 周期性任务执行成功，执行次数: {counter['count']}")
except Exception as e:
    print(f"❌ 周期性任务执行失败: {e}")

# 测试7：验证任务取消
print("\n[测试7] 验证任务取消")
try:
    scheduler = TaskScheduler()

    def dummy():
        return "dummy"

    task_id = scheduler.schedule_once(dummy, time.time() + 10, priority=5)
    assert scheduler.cancel_task(task_id) is True
    assert scheduler.scheduled_tasks[task_id]["status"] == "cancelled"
    print("✅ 任务取消成功")
except Exception as e:
    print(f"❌ 任务取消失败: {e}")

# 测试8：验证任务移除
print("\n[测试8] 验证任务移除")
try:
    scheduler = TaskScheduler()

    def dummy2():
        return "dummy2"

    task_id = scheduler.schedule_once(dummy2, time.time() + 10, priority=5)
    assert scheduler.remove_task(task_id) is True
    assert task_id not in scheduler.scheduled_tasks
    print("✅ 任务移除成功")
except Exception as e:
    print(f"❌ 任务移除失败: {e}")

# 测试9：验证集成到FirstPrincipleEternalAgent
print("\n[测试9] 验证集成到FirstPrincipleEternalAgent")
try:
    agent = FirstPrincipleEternalAgent()
    assert hasattr(agent, 'task_scheduler')
    assert agent.task_scheduler is not None
    assert isinstance(agent.task_scheduler, TaskScheduler)
    print("✅ Agent集成TaskScheduler成功")
    print(f"   task_scheduler类型: {type(agent.task_scheduler).__name__}")
except Exception as e:
    print(f"❌ Agent集成测试失败: {e}")

# 测试10：验证任务列表功能
print("\n[测试10] 验证任务列表功能")
try:
    scheduler = TaskScheduler()
    scheduler.schedule_once(lambda: "a", time.time() + 1, priority=5)
    scheduler.schedule_periodic(lambda: "b", interval=2, priority=3)
    tasks = scheduler.list_tasks()
    assert "scheduled" in tasks
    assert "periodic" in tasks
    assert len(tasks["scheduled"]) == 1
    assert len(tasks["periodic"]) == 1
    print("✅ 任务列表功能正常")
except Exception as e:
    print(f"❌ 任务列表功能失败: {e}")

print("\n" + "=" * 60)
print("阶段27测试完成！")
print("=" * 60)
