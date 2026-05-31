#!/usr/bin/env python3
"""
阶段48测试：验证消息队列（MessageQueue类）
"""
import sys
import os
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from first_principles_agent import MessageQueue

print("=" * 60)
print("阶段48测试：消息队列（MessageQueue类）")
print("=" * 60)

# 测试1：验证MessageQueue初始化
print("\n[测试1] 验证MessageQueue初始化")
try:
    mq = MessageQueue(max_size=100)
    assert mq.max_size == 100
    print("✅ MessageQueue初始化成功")
except Exception as e:
    print(f"❌ MessageQueue初始化失败: {e}")

# 测试2：验证publish
print("\n[测试2] 验证publish")
try:
    mq = MessageQueue()
    mq.publish("test_queue", "message1")
    assert mq.queue_size("test_queue") == 1
    print("✅ publish正常")
except Exception as e:
    print(f"❌ publish测试失败: {e}")

# 测试3：验证consume
print("\n[测试3] 验证consume")
try:
    mq = MessageQueue()
    mq.publish("test_queue", "msg1")
    mq.publish("test_queue", "msg2")
    msg = mq.consume("test_queue")
    assert msg == "msg1"
    assert mq.queue_size("test_queue") == 1
    print("✅ consume正常")
except Exception as e:
    print(f"❌ consume测试失败: {e}")

# 测试4：验证subscribe
print("\n[测试4] 验证subscribe")
try:
    mq = MessageQueue()
    received = []
    def callback(msg):
        received.append(msg)
    mq.subscribe("events", callback)
    mq.publish("events", "event1")
    assert len(received) == 1
    assert received[0] == "event1"
    print("✅ subscribe正常")
except Exception as e:
    print(f"❌ subscribe测试失败: {e}")

# 测试5：验证多个订阅者
print("\n[测试5] 验证多个订阅者")
try:
    mq = MessageQueue()
    r1 = []
    r2 = []
    mq.subscribe("multi", lambda m: r1.append(m))
    mq.subscribe("multi", lambda m: r2.append(m))
    mq.publish("multi", "test")
    assert len(r1) == 1
    assert len(r2) == 1
    print("✅ 多个订阅者正常")
except Exception as e:
    print(f"❌ 多个订阅者测试失败: {e}")

# 测试6：验证list_queues
print("\n[测试6] 验证list_queues")
try:
    mq = MessageQueue()
    mq.publish("q1", "a")
    mq.publish("q2", "b")
    queues = mq.list_queues()
    assert "q1" in queues
    assert "q2" in queues
    print(f"✅ list_queues正常: {queues}")
except Exception as e:
    print(f"❌ list_queues测试失败: {e}")

# 测试7：验证clear_queue
print("\n[测试7] 验证clear_queue")
try:
    mq = MessageQueue()
    mq.publish("clear_me", "a")
    mq.publish("clear_me", "b")
    assert mq.queue_size("clear_me") == 2
    mq.clear_queue("clear_me")
    assert mq.queue_size("clear_me") == 0
    print("✅ clear_queue正常")
except Exception as e:
    print(f"❌ clear_queue测试失败: {e}")

# 测试8：验证空队列consume
print("\n[测试8] 验证空队列consume")
try:
    mq = MessageQueue()
    result = mq.consume("empty_queue")
    assert result is None
    print("✅ 空队列consume正常")
except Exception as e:
    print(f"❌ 空队列consume测试失败: {e}")

# 测试9：验证持久化
print("\n[测试9] 验证持久化")
try:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as f:
        path = f.name
    mq = MessageQueue(persistent_path=path)
    mq.publish("persist", "data1")
    mq.publish("persist", "data2")
    mq2 = MessageQueue(persistent_path=path)
    assert mq2.queue_size("persist") == 2
    assert mq2.consume("persist") == "data1"
    os.remove(path)
    print("✅ 持久化正常")
except Exception as e:
    print(f"❌ 持久化测试失败: {e}")

# 测试10：验证队列大小限制
print("\n[测试10] 验证队列大小限制")
try:
    mq = MessageQueue(max_size=3)
    mq.publish("limited", "a")
    mq.publish("limited", "b")
    mq.publish("limited", "c")
    mq.publish("limited", "d")
    assert mq.queue_size("limited") == 3
    print("✅ 队列大小限制正常")
except Exception as e:
    print(f"❌ 队列大小限制测试失败: {e}")

# 测试11：验证不同队列隔离
print("\n[测试11] 验证不同队列隔离")
try:
    mq = MessageQueue()
    mq.publish("q1", "only_in_q1")
    mq.publish("q2", "only_in_q2")
    assert mq.consume("q1") == "only_in_q1"
    assert mq.consume("q2") == "only_in_q2"
    print("✅ 不同队列隔离正常")
except Exception as e:
    print(f"❌ 不同队列隔离测试失败: {e}")

# 测试12：验证订阅者异常处理
print("\n[测试12] 验证订阅者异常处理")
try:
    mq = MessageQueue()
    def bad_callback(msg):
        raise RuntimeError("bad")
    mq.subscribe("errors", bad_callback)
    result = mq.publish("errors", "test")
    assert result is True
    print("✅ 订阅者异常处理正常")
except Exception as e:
    print(f"❌ 订阅者异常处理测试失败: {e}")

print("\n" + "=" * 60)
print("阶段48测试完成！")
print("=" * 60)
