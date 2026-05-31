#!/usr/bin/env python3
"""
阶段31测试：验证缓存系统（Cache类）
"""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from first_principles_agent import Cache, FirstPrincipleKG

print("=" * 60)
print("阶段31测试：缓存系统（Cache类）")
print("=" * 60)

# 测试1：验证Cache初始化
print("\n[测试1] 验证Cache初始化")
try:
    cache = Cache(max_size=10, default_ttl=60)
    assert cache.max_size == 10
    assert cache.default_ttl == 60
    assert cache.size() == 0
    print("✅ Cache初始化成功")
except Exception as e:
    print(f"❌ Cache初始化失败: {e}")

# 测试2：验证基本set/get
print("\n[测试2] 验证基本set/get")
try:
    cache = Cache()
    cache.set("key1", "value1")
    assert cache.get("key1") == "value1"
    print("✅ 基本set/get正常")
except Exception as e:
    print(f"❌ 基本set/get失败: {e}")

# 测试3：验证获取不存在的key
print("\n[测试3] 验证获取不存在的key")
try:
    cache = Cache()
    assert cache.get("nonexistent") is None
    assert cache.get("nonexistent", "default") == "default"
    print("✅ 获取不存在的key正常")
except Exception as e:
    print(f"❌ 获取不存在的key失败: {e}")

# 测试4：验证TTL过期
print("\n[测试4] 验证TTL过期")
try:
    cache = Cache()
    cache.set("key2", "value2", ttl=0.1)
    assert cache.get("key2") == "value2"
    time.sleep(0.2)
    assert cache.get("key2") is None
    print("✅ TTL过期正常")
except Exception as e:
    print(f"❌ TTL过期测试失败: {e}")

# 测试5：验证LRU淘汰
print("\n[测试5] 验证LRU淘汰")
try:
    cache = Cache(max_size=3)
    cache.set("a", 1)
    cache.set("b", 2)
    cache.set("c", 3)
    cache.set("d", 4)
    assert cache.get("a") is None
    assert cache.get("b") == 2
    assert cache.get("c") == 3
    assert cache.get("d") == 4
    print("✅ LRU淘汰正常")
except Exception as e:
    print(f"❌ LRU淘汰测试失败: {e}")

# 测试6：验证LRU访问顺序更新
print("\n[测试6] 验证LRU访问顺序更新")
try:
    cache = Cache(max_size=3)
    cache.set("a", 1)
    cache.set("b", 2)
    cache.set("c", 3)
    cache.get("a")
    cache.set("d", 4)
    assert cache.get("a") == 1
    assert cache.get("b") is None
    print("✅ LRU访问顺序更新正常")
except Exception as e:
    print(f"❌ LRU访问顺序更新测试失败: {e}")

# 测试7：验证delete
print("\n[测试7] 验证delete")
try:
    cache = Cache()
    cache.set("del", "val")
    assert cache.delete("del") is True
    assert cache.get("del") is None
    assert cache.delete("nonexistent") is False
    print("✅ delete正常")
except Exception as e:
    print(f"❌ delete测试失败: {e}")

# 测试8：验证clear
print("\n[测试8] 验证clear")
try:
    cache = Cache()
    cache.set("x", 1)
    cache.set("y", 2)
    cache.clear()
    assert cache.size() == 0
    assert cache.get("x") is None
    print("✅ clear正常")
except Exception as e:
    print(f"❌ clear测试失败: {e}")

# 测试9：验证stats统计
print("\n[测试9] 验证stats统计")
try:
    cache = Cache()
    cache.set("k1", "v1")
    cache.get("k1")
    cache.get("k1")
    cache.get("missing")
    stats = cache.stats()
    assert stats["size"] == 1
    assert stats["hit_count"] == 2
    assert stats["miss_count"] == 1
    assert stats["access_count"] == 3
    assert stats["hit_rate"] == 66.67
    print(f"✅ stats统计正常: {stats}")
except Exception as e:
    print(f"❌ stats统计测试失败: {e}")

# 测试10：验证keys/values/items
print("\n[测试10] 验证keys/values/items")
try:
    cache = Cache()
    cache.set("k1", "v1")
    cache.set("k2", "v2")
    assert "k1" in cache.keys()
    assert "v1" in cache.values()
    assert ("k1", "v1") in cache.items()
    print("✅ keys/values/items正常")
except Exception as e:
    print(f"❌ keys/values/items测试失败: {e}")

# 测试11：验证集成到FirstPrincipleKG
print("\n[测试11] 验证集成到FirstPrincipleKG")
try:
    kg = FirstPrincipleKG()
    assert hasattr(kg, 'cache')
    assert isinstance(kg.cache, Cache)
    insights1 = kg.get_insights()
    insights2 = kg.get_insights()
    assert insights1 == insights2
    print("✅ FirstPrincipleKG集成Cache成功")
except Exception as e:
    print(f"❌ FirstPrincipleKG集成测试失败: {e}")

# 测试12：验证缓存命中
print("\n[测试12] 验证缓存命中")
try:
    kg = FirstPrincipleKG()
    kg.cache.clear()
    kg._invalidate_insights_cache()
    kg.cache.set("test_key", {"data": 123}, ttl=60)
    result = kg.cache.get("test_key")
    assert result == {"data": 123}
    print("✅ 缓存命中正常")
except Exception as e:
    print(f"❌ 缓存命中测试失败: {e}")

print("\n" + "=" * 60)
print("阶段31测试完成！")
print("=" * 60)
