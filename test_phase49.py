#!/usr/bin/env python3
"""
阶段49测试：验证缓存策略（CacheStrategy类）
"""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from first_principles_agent import CacheStrategy

print("=" * 60)
print("阶段49测试：缓存策略（CacheStrategy类）")
print("=" * 60)

# 测试1：验证CacheStrategy初始化
print("\n[测试1] 验证CacheStrategy初始化")
try:
    cs = CacheStrategy(max_size=10, strategy="lru")
    assert cs.max_size == 10
    assert cs.strategy == "lru"
    print("✅ CacheStrategy初始化成功")
except Exception as e:
    print(f"❌ CacheStrategy初始化失败: {e}")

# 测试2：验证LRU策略
print("\n[测试2] 验证LRU策略")
try:
    cs = CacheStrategy(max_size=3, strategy="lru")
    cs.set("a", 1)
    cs.set("b", 2)
    cs.set("c", 3)
    cs.get("a")
    cs.set("d", 4)
    assert cs.get("a") == 1
    assert cs.get("b") is None
    print("✅ LRU策略正常")
except Exception as e:
    print(f"❌ LRU策略测试失败: {e}")

# 测试3：验证LFU策略
print("\n[测试3] 验证LFU策略")
try:
    cs = CacheStrategy(max_size=3, strategy="lfu")
    cs.set("a", 1)
    cs.set("b", 2)
    cs.set("c", 3)
    cs.get("a")
    cs.get("a")
    cs.get("b")
    cs.set("d", 4)
    assert cs.get("a") == 1
    assert cs.get("c") is None
    print("✅ LFU策略正常")
except Exception as e:
    print(f"❌ LFU策略测试失败: {e}")

# 测试4：验证FIFO策略
print("\n[测试4] 验证FIFO策略")
try:
    cs = CacheStrategy(max_size=3, strategy="fifo")
    cs.set("a", 1)
    cs.set("b", 2)
    cs.set("c", 3)
    cs.set("d", 4)
    assert cs.get("a") is None
    assert cs.get("b") == 2
    print("✅ FIFO策略正常")
except Exception as e:
    print(f"❌ FIFO策略测试失败: {e}")

# 测试5：验证RANDOM策略
print("\n[测试5] 验证RANDOM策略")
try:
    cs = CacheStrategy(max_size=3, strategy="random")
    cs.set("a", 1)
    cs.set("b", 2)
    cs.set("c", 3)
    cs.set("d", 4)
    assert cs.stats()["size"] == 3
    print("✅ RANDOM策略正常")
except Exception as e:
    print(f"❌ RANDOM策略测试失败: {e}")

# 测试6：验证get/set
print("\n[测试6] 验证get/set")
try:
    cs = CacheStrategy()
    cs.set("key", "value")
    assert cs.get("key") == "value"
    assert cs.get("missing") is None
    print("✅ get/set正常")
except Exception as e:
    print(f"❌ get/set测试失败: {e}")

# 测试7：验证delete
print("\n[测试7] 验证delete")
try:
    cs = CacheStrategy()
    cs.set("del", "val")
    assert cs.delete("del") is True
    assert cs.get("del") is None
    assert cs.delete("missing") is False
    print("✅ delete正常")
except Exception as e:
    print(f"❌ delete测试失败: {e}")

# 测试8：验证clear
print("\n[测试8] 验证clear")
try:
    cs = CacheStrategy()
    cs.set("a", 1)
    cs.set("b", 2)
    cs.clear()
    assert cs.stats()["size"] == 0
    assert cs.get("a") is None
    print("✅ clear正常")
except Exception as e:
    print(f"❌ clear测试失败: {e}")

# 测试9：验证warm_up
print("\n[测试9] 验证warm_up")
try:
    cs = CacheStrategy()
    cs.warm_up({"k1": "v1", "k2": "v2", "k3": "v3"})
    assert cs.get("k1") == "v1"
    assert cs.get("k2") == "v2"
    assert cs.get("k3") == "v3"
    print("✅ warm_up正常")
except Exception as e:
    print(f"❌ warm_up测试失败: {e}")

# 测试10：验证stats
print("\n[测试10] 验证stats")
try:
    cs = CacheStrategy(max_size=5, strategy="lru")
    cs.set("a", 1)
    cs.set("b", 2)
    cs.get("a")
    stats = cs.stats()
    assert stats["size"] == 2
    assert stats["max_size"] == 5
    assert stats["strategy"] == "lru"
    assert "a" in stats["keys"]
    assert stats["access_stats"]["a"] == 1
    print(f"✅ stats正常: {stats}")
except Exception as e:
    print(f"❌ stats测试失败: {e}")

# 测试11：验证不支持策略
print("\n[测试11] 验证不支持策略")
try:
    try:
        cs = CacheStrategy(strategy="invalid")
        print("❌ 应该抛出异常")
    except ValueError as e:
        assert "不支持" in str(e)
        print("✅ 不支持策略正确抛出异常")
except Exception as e:
    print(f"❌ 不支持策略测试失败: {e}")

# 测试12：验证更新已有key
print("\n[测试12] 验证更新已有key")
try:
    cs = CacheStrategy()
    cs.set("key", "old")
    cs.set("key", "new")
    assert cs.get("key") == "new"
    print("✅ 更新已有key正常")
except Exception as e:
    print(f"❌ 更新已有key测试失败: {e}")

print("\n" + "=" * 60)
print("阶段49测试完成！")
print("=" * 60)
