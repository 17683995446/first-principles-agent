#!/usr/bin/env python3
"""
阶段46测试：验证线程工具（ThreadUtils类）
"""
import sys
import os
import time
import threading

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from first_principles_agent import ThreadUtils

print("=" * 60)
print("阶段46测试：线程工具（ThreadUtils类）")
print("=" * 60)

# 测试1：验证ThreadUtils初始化
print("\n[测试1] 验证ThreadUtils初始化")
try:
    tu = ThreadUtils(max_workers=4)
    assert tu.max_workers == 4
    print("✅ ThreadUtils初始化成功")
except Exception as e:
    print(f"❌ ThreadUtils初始化失败: {e}")

# 测试2：验证submit
print("\n[测试2] 验证submit")
try:
    tu = ThreadUtils()
    results = []
    def task():
        results.append(1)
        return "done"
    tid = tu.submit(task)
    tu.wait_all()
    assert len(results) == 1
    print(f"✅ submit正常: {tid}")
except Exception as e:
    print(f"❌ submit测试失败: {e}")

# 测试3：验证submit返回值
print("\n[测试3] 验证submit返回值")
try:
    tu = ThreadUtils()
    def task():
        return 42
    tu.submit(task)
    tu.wait_all()
    results = tu.get_results()
    assert len(results) > 0
    success = any(r.get("result") == 42 for r in results.values())
    assert success
    print("✅ submit返回值正常")
except Exception as e:
    print(f"❌ submit返回值测试失败: {e}")

# 测试4：验证submit异常处理
print("\n[测试4] 验证submit异常处理")
try:
    tu = ThreadUtils()
    def bad_task():
        raise ValueError("test error")
    tu.submit(bad_task)
    tu.wait_all()
    results = tu.get_results()
    has_error = any(not r.get("success") for r in results.values())
    assert has_error
    print("✅ submit异常处理正常")
except Exception as e:
    print(f"❌ submit异常处理测试失败: {e}")

# 测试5：验证map
print("\n[测试5] 验证map")
try:
    tu = ThreadUtils()
    results = []
    def process(x):
        results.append(x)
    tu.map(process, [1, 2, 3])
    assert sorted(results) == [1, 2, 3]
    print("✅ map正常")
except Exception as e:
    print(f"❌ map测试失败: {e}")

# 测试6：验证active_count
print("\n[测试6] 验证active_count")
try:
    tu = ThreadUtils()
    def slow_task():
        time.sleep(0.2)
    tu.submit(slow_task)
    time.sleep(0.05)
    count = tu.active_count()
    assert count >= 0
    tu.wait_all()
    assert tu.active_count() == 0
    print(f"✅ active_count正常")
except Exception as e:
    print(f"❌ active_count测试失败: {e}")

# 测试7：验证clear_results
print("\n[测试7] 验证clear_results")
try:
    tu = ThreadUtils()
    def task():
        return 1
    tu.submit(task)
    tu.wait_all()
    assert len(tu.get_results()) > 0
    tu.clear_results()
    assert len(tu.get_results()) == 0
    print("✅ clear_results正常")
except Exception as e:
    print(f"❌ clear_results测试失败: {e}")

# 测试8：验证current_thread_name
print("\n[测试8] 验证current_thread_name")
try:
    name = ThreadUtils.current_thread_name()
    assert isinstance(name, str)
    assert len(name) > 0
    print(f"✅ current_thread_name正常: {name}")
except Exception as e:
    print(f"❌ current_thread_name测试失败: {e}")

# 测试9：验证sleep
print("\n[测试9] 验证sleep")
try:
    start = time.time()
    ThreadUtils.sleep(0.1)
    elapsed = time.time() - start
    assert elapsed >= 0.08
    print(f"✅ sleep正常: {elapsed:.3f}s")
except Exception as e:
    print(f"❌ sleep测试失败: {e}")

# 测试10：验证lock
print("\n[测试10] 验证lock")
try:
    lock = ThreadUtils.lock()
    assert lock is not None
    with lock:
        pass
    print("✅ lock正常")
except Exception as e:
    print(f"❌ lock测试失败: {e}")

# 测试11：验证多任务并发
print("\n[测试11] 验证多任务并发")
try:
    tu = ThreadUtils()
    counter = {"value": 0}
    lock = threading.Lock()
    def increment():
        with lock:
            counter["value"] += 1
    import threading
    for _ in range(10):
        tu.submit(increment)
    tu.wait_all()
    assert counter["value"] == 10
    print(f"✅ 多任务并发正常: counter={counter['value']}")
except Exception as e:
    print(f"❌ 多任务并发测试失败: {e}")

# 测试12：验证wait_all超时
print("\n[测试12] 验证wait_all")
try:
    tu = ThreadUtils()
    def task():
        time.sleep(0.05)
        return 1
    for _ in range(3):
        tu.submit(task)
    tu.wait_all()
    assert tu.active_count() == 0
    print("✅ wait_all正常")
except Exception as e:
    print(f"❌ wait_all测试失败: {e}")

print("\n" + "=" * 60)
print("阶段46测试完成！")
print("=" * 60)
