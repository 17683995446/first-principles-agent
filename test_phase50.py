#!/usr/bin/env python3
"""
阶段50测试：验证连接池（ConnectionPool类）
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from first_principles_agent import ConnectionPool

print("=" * 60)
print("阶段50测试：连接池（ConnectionPool类）")
print("=" * 60)

# 测试1：验证ConnectionPool初始化
print("\n[测试1] 验证ConnectionPool初始化")
try:
    def factory():
        return {"connected": True}
    pool = ConnectionPool(factory, max_size=5, timeout=10)
    assert pool.max_size == 5
    assert pool.timeout == 10
    print("✅ ConnectionPool初始化成功")
except Exception as e:
    print(f"❌ ConnectionPool初始化失败: {e}")

# 测试2：验证acquire
print("\n[测试2] 验证acquire")
try:
    def factory():
        return {"connected": True}
    pool = ConnectionPool(factory, max_size=2)
    conn1 = pool.acquire()
    assert conn1 is not None
    assert conn1["connected"] is True
    print("✅ acquire正常")
except Exception as e:
    print(f"❌ acquire测试失败: {e}")

# 测试3：验证release
print("\n[测试3] 验证release")
try:
    def factory():
        return {"connected": True}
    pool = ConnectionPool(factory, max_size=2)
    conn = pool.acquire()
    result = pool.release(conn)
    assert result is True
    stats = pool.stats()
    assert stats["available"] == 1
    print("✅ release正常")
except Exception as e:
    print(f"❌ release测试失败: {e}")

# 测试4：验证连接复用
print("\n[测试4] 验证连接复用")
try:
    def factory():
        return {"id": id(object())}
    pool = ConnectionPool(factory, max_size=2)
    conn1 = pool.acquire()
    pool.release(conn1)
    conn2 = pool.acquire()
    assert conn1 is conn2
    pool.release(conn2)
    print("✅ 连接复用正常")
except Exception as e:
    print(f"❌ 连接复用测试失败: {e}")

# 测试5：验证stats
print("\n[测试5] 验证stats")
try:
    def factory():
        return {"connected": True}
    pool = ConnectionPool(factory, max_size=3)
    conn1 = pool.acquire()
    conn2 = pool.acquire()
    stats = pool.stats()
    assert stats["max_size"] == 3
    assert stats["in_use"] == 2
    assert stats["created"] == 2
    pool.release(conn1)
    pool.release(conn2)
    print(f"✅ stats正常: {stats}")
except Exception as e:
    print(f"❌ stats测试失败: {e}")

# 测试6：验证close
print("\n[测试6] 验证close")
try:
    closed = []
    class Conn:
        def close(self):
            closed.append(1)
    def factory():
        return Conn()
    pool = ConnectionPool(factory, max_size=2)
    conn = pool.acquire()
    pool.close(conn)
    stats = pool.stats()
    assert stats["in_use"] == 0
    assert len(closed) == 1
    print("✅ close正常")
except Exception as e:
    print(f"❌ close测试失败: {e}")

# 测试7：验证close_all
print("\n[测试7] 验证close_all")
try:
    closed = []
    class Conn:
        def close(self):
            closed.append(1)
    def factory():
        return Conn()
    pool = ConnectionPool(factory, max_size=3)
    conn1 = pool.acquire()
    conn2 = pool.acquire()
    pool.release(conn1)
    pool.close_all()
    stats = pool.stats()
    assert stats["created"] == 0
    assert stats["available"] == 0
    assert stats["in_use"] == 0
    print("✅ close_all正常")
except Exception as e:
    print(f"❌ close_all测试失败: {e}")

# 测试8：验证超时
print("\n[测试8] 验证超时")
try:
    def factory():
        return {"connected": True}
    pool = ConnectionPool(factory, max_size=1, timeout=0.1)
    conn = pool.acquire()
    try:
        pool.acquire()
        print("❌ 应该超时")
    except TimeoutError:
        print("✅ 超时正常")
    pool.release(conn)
except Exception as e:
    print(f"❌ 超时测试失败: {e}")

# 测试9：验证最大连接数限制
print("\n[测试9] 验证最大连接数限制")
try:
    def factory():
        return {"connected": True}
    pool = ConnectionPool(factory, max_size=2)
    conn1 = pool.acquire()
    conn2 = pool.acquire()
    stats = pool.stats()
    assert stats["created"] == 2
    pool.release(conn1)
    pool.release(conn2)
    print("✅ 最大连接数限制正常")
except Exception as e:
    print(f"❌ 最大连接数限制测试失败: {e}")

# 测试10：验证健康检查
print("\n[测试10] 验证健康检查")
try:
    class HealthyConn:
        def healthy(self):
            return True
    def factory():
        return HealthyConn()
    pool = ConnectionPool(factory, max_size=2)
    conn = pool.acquire()
    assert conn is not None
    pool.release(conn)
    conn2 = pool.acquire()
    assert conn2 is not None
    pool.release(conn2)
    stats = pool.stats()
    assert stats["health_checks"] >= 1
    print("✅ 健康检查正常")
except Exception as e:
    print(f"❌ 健康检查测试失败: {e}")

# 测试11：验证释放未使用的连接
print("\n[测试11] 验证释放未使用的连接")
try:
    def factory():
        return {"connected": True}
    pool = ConnectionPool(factory, max_size=2)
    conn = pool.acquire()
    result = pool.release({})
    assert result is False
    pool.release(conn)
    print("✅ 释放未使用的连接正常")
except Exception as e:
    print(f"❌ 释放未使用的连接测试失败: {e}")

# 测试12：验证多次acquire/release
print("\n[测试12] 验证多次acquire/release")
try:
    def factory():
        return {"connected": True}
    pool = ConnectionPool(factory, max_size=2)
    for i in range(5):
        conn = pool.acquire()
        assert conn is not None
        pool.release(conn)
    stats = pool.stats()
    assert stats["created"] <= 2
    print("✅ 多次acquire/release正常")
except Exception as e:
    print(f"❌ 多次acquire/release测试失败: {e}")

print("\n" + "=" * 60)
print("阶段50测试完成！")
print("=" * 60)
