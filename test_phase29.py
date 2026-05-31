#!/usr/bin/env python3
"""
阶段29测试：验证事件系统（EventSystem类）
"""
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from first_principles_agent import EventSystem, FirstPrincipleEternalAgent

print("=" * 60)
print("阶段29测试：事件系统（EventSystem类）")
print("=" * 60)

# 测试1：验证EventSystem初始化
print("\n[测试1] 验证EventSystem初始化")
try:
    es = EventSystem()
    assert es.listeners == {}
    assert es.once_listeners == {}
    print("✅ EventSystem初始化成功")
except Exception as e:
    print(f"❌ EventSystem初始化失败: {e}")

# 测试2：验证事件订阅（on）
print("\n[测试2] 验证事件订阅（on）")
try:
    es = EventSystem()
    received = []

    def listener1(data):
        received.append(data)

    es.on("test_event", listener1)
    assert es.listener_count("test_event") == 1
    print("✅ 事件订阅成功")
except Exception as e:
    print(f"❌ 事件订阅测试失败: {e}")

# 测试3：验证事件发布（emit）
print("\n[测试3] 验证事件发布（emit）")
try:
    es = EventSystem()
    received = []

    def listener2(data):
        received.append(data)
        return f"received_{data}"

    es.on("test_event", listener2)
    results = es.emit("test_event", "hello")
    assert len(received) == 1
    assert received[0] == "hello"
    assert results[0] == "received_hello"
    print("✅ 事件发布成功")
    print(f"   接收数据: {received}")
    print(f"   返回结果: {results}")
except Exception as e:
    print(f"❌ 事件发布测试失败: {e}")

# 测试4：验证多个监听器
print("\n[测试4] 验证多个监听器")
try:
    es = EventSystem()
    count = {"value": 0}

    def inc1():
        count["value"] += 1

    def inc2():
        count["value"] += 10

    es.on("multi", inc1)
    es.on("multi", inc2)
    es.emit("multi")
    assert count["value"] == 11
    print("✅ 多个监听器测试通过")
    print(f"   计数结果: {count['value']}")
except Exception as e:
    print(f"❌ 多个监听器测试失败: {e}")

# 测试5：验证一次性监听器（once）
print("\n[测试5] 验证一次性监听器（once）")
try:
    es = EventSystem()
    calls = {"count": 0}

    def once_listener():
        calls["count"] += 1

    es.once("once_event", once_listener)
    es.emit("once_event")
    es.emit("once_event")
    assert calls["count"] == 1
    assert es.listener_count("once_event") == 0
    print("✅ 一次性监听器测试通过")
    print(f"   调用次数: {calls['count']}")
except Exception as e:
    print(f"❌ 一次性监听器测试失败: {e}")

# 测试6：验证注销指定监听器（off）
print("\n[测试6] 验证注销指定监听器（off）")
try:
    es = EventSystem()

    def listener_a():
        pass

    def listener_b():
        pass

    es.on("off_test", listener_a)
    es.on("off_test", listener_b)
    assert es.listener_count("off_test") == 2

    es.off("off_test", listener_a)
    assert es.listener_count("off_test") == 1
    print("✅ 注销指定监听器测试通过")
except Exception as e:
    print(f"❌ 注销指定监听器测试失败: {e}")

# 测试7：验证注销事件所有监听器（off无listener参数）
print("\n[测试7] 验证注销事件所有监听器")
try:
    es = EventSystem()

    def listener_c():
        pass

    es.on("clear_test", listener_c)
    es.once("clear_test", listener_c)
    assert es.listener_count("clear_test") == 2

    es.off("clear_test")
    assert es.listener_count("clear_test") == 0
    print("✅ 注销事件所有监听器测试通过")
except Exception as e:
    print(f"❌ 注销事件所有监听器测试失败: {e}")

# 测试8：验证事件参数传递
print("\n[测试8] 验证事件参数传递")
try:
    es = EventSystem()
    captured = {}

    def capture_listener(a, b, c=None):
        captured["a"] = a
        captured["b"] = b
        captured["c"] = c

    es.on("args_test", capture_listener)
    es.emit("args_test", 1, 2, c=3)
    assert captured["a"] == 1
    assert captured["b"] == 2
    assert captured["c"] == 3
    print("✅ 事件参数传递测试通过")
    print(f"   捕获参数: {captured}")
except Exception as e:
    print(f"❌ 事件参数传递测试失败: {e}")

# 测试9：验证集成到FirstPrincipleEternalAgent
print("\n[测试9] 验证集成到FirstPrincipleEternalAgent")
try:
    agent = FirstPrincipleEternalAgent()
    assert hasattr(agent, 'event_system')
    assert agent.event_system is not None
    assert isinstance(agent.event_system, EventSystem)
    print("✅ Agent集成EventSystem成功")
    print(f"   event_system类型: {type(agent.event_system).__name__}")
except Exception as e:
    print(f"❌ Agent集成测试失败: {e}")

# 测试10：验证事件名称列表和清除
print("\n[测试10] 验证事件名称列表和清除")
try:
    es = EventSystem()

    def dummy():
        pass

    es.on("event1", dummy)
    es.on("event2", dummy)
    names = es.event_names()
    assert "event1" in names
    assert "event2" in names
    print("✅ 事件名称列表正常")

    es.clear()
    assert es.event_names() == []
    assert es.listeners == {}
    assert es.once_listeners == {}
    print("✅ 清除所有监听器正常")
except Exception as e:
    print(f"❌ 事件名称列表和清除测试失败: {e}")

# 测试11：验证监听器异常处理
print("\n[测试11] 验证监听器异常处理")
try:
    es = EventSystem()

    def error_listener():
        raise ValueError("测试异常")

    es.on("error_event", error_listener)
    results = es.emit("error_event")
    assert len(results) == 1
    assert "error" in results[0]
    print("✅ 监听器异常处理正常")
except Exception as e:
    print(f"❌ 监听器异常处理测试失败: {e}")

print("\n" + "=" * 60)
print("阶段29测试完成！")
print("=" * 60)
