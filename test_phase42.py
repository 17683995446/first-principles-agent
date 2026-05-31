#!/usr/bin/env python3
"""
阶段42测试：验证集合工具（CollectionUtils类）
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from first_principles_agent import CollectionUtils

print("=" * 60)
print("阶段42测试：集合工具（CollectionUtils类）")
print("=" * 60)

# 测试1：验证unique
print("\n[测试1] 验证unique")
try:
    result = CollectionUtils.unique([1, 2, 2, 3, 3, 3])
    assert result == [1, 2, 3]
    print(f"✅ unique正常: {result}")
except Exception as e:
    print(f"❌ unique测试失败: {e}")

# 测试2：验证flatten
print("\n[测试2] 验证flatten")
try:
    result = CollectionUtils.flatten([1, [2, 3], [4, [5, 6]]])
    assert result == [1, 2, 3, 4, 5, 6]
    print(f"✅ flatten正常: {result}")
except Exception as e:
    print(f"❌ flatten测试失败: {e}")

# 测试3：验证chunk
print("\n[测试3] 验证chunk")
try:
    result = CollectionUtils.chunk([1, 2, 3, 4, 5], 2)
    assert result == [[1, 2], [3, 4], [5]]
    print(f"✅ chunk正常: {result}")
except Exception as e:
    print(f"❌ chunk测试失败: {e}")

# 测试4：验证group_by
print("\n[测试4] 验证group_by")
try:
    data = [{"type": "a", "val": 1}, {"type": "b", "val": 2}, {"type": "a", "val": 3}]
    result = CollectionUtils.group_by(data, lambda x: x["type"])
    assert "a" in result
    assert "b" in result
    assert len(result["a"]) == 2
    print(f"✅ group_by正常: {list(result.keys())}")
except Exception as e:
    print(f"❌ group_by测试失败: {e}")

# 测试5：验证sort_by
print("\n[测试5] 验证sort_by")
try:
    data = [{"age": 30}, {"age": 20}, {"age": 40}]
    result = CollectionUtils.sort_by(data, lambda x: x["age"])
    assert result[0]["age"] == 20
    assert result[-1]["age"] == 40
    print(f"✅ sort_by正常: {[x['age'] for x in result]}")
except Exception as e:
    print(f"❌ sort_by测试失败: {e}")

# 测试6：验证top_n
print("\n[测试6] 验证top_n")
try:
    data = [3, 1, 4, 1, 5, 9, 2, 6]
    result = CollectionUtils.top_n(data, 3)
    assert result == [9, 6, 5]
    print(f"✅ top_n正常: {result}")
except Exception as e:
    print(f"❌ top_n测试失败: {e}")

# 测试7：验证binary_search
print("\n[测试7] 验证binary_search")
try:
    data = [1, 3, 5, 7, 9]
    assert CollectionUtils.binary_search(data, 5) == 2
    assert CollectionUtils.binary_search(data, 10) == -1
    print("✅ binary_search正常")
except Exception as e:
    print(f"❌ binary_search测试失败: {e}")

# 测试8：验证filter_by
print("\n[测试8] 验证filter_by")
try:
    data = [1, 2, 3, 4, 5]
    result = CollectionUtils.filter_by(data, lambda x: x > 3)
    assert result == [4, 5]
    print(f"✅ filter_by正常: {result}")
except Exception as e:
    print(f"❌ filter_by测试失败: {e}")

# 测试9：验证map_to
print("\n[测试9] 验证map_to")
try:
    data = [1, 2, 3]
    result = CollectionUtils.map_to(data, lambda x: x * 2)
    assert result == [2, 4, 6]
    print(f"✅ map_to正常: {result}")
except Exception as e:
    print(f"❌ map_to测试失败: {e}")

# 测试10：验证binary_search带key_func
print("\n[测试10] 验证binary_search带key_func")
try:
    data = [{"id": 1}, {"id": 3}, {"id": 5}]
    result = CollectionUtils.binary_search(data, 3, lambda x: x["id"])
    assert result == 1
    print("✅ binary_search带key_func正常")
except Exception as e:
    print(f"❌ binary_search带key_func测试失败: {e}")

# 测试11：验证top_n带key_func
print("\n[测试11] 验证top_n带key_func")
try:
    data = [{"score": 50}, {"score": 90}, {"score": 70}]
    result = CollectionUtils.top_n(data, 2, lambda x: x["score"])
    assert result[0]["score"] == 90
    assert result[1]["score"] == 70
    print(f"✅ top_n带key_func正常")
except Exception as e:
    print(f"❌ top_n带key_func测试失败: {e}")

# 测试12：验证空集合处理
print("\n[测试12] 验证空集合处理")
try:
    assert CollectionUtils.unique([]) == []
    assert CollectionUtils.flatten([]) == []
    assert CollectionUtils.chunk([], 2) == []
    assert CollectionUtils.sort_by([], lambda x: x) == []
    assert CollectionUtils.filter_by([], lambda x: True) == []
    print("✅ 空集合处理正常")
except Exception as e:
    print(f"❌ 空集合处理测试失败: {e}")

print("\n" + "=" * 60)
print("阶段42测试完成！")
print("=" * 60)
