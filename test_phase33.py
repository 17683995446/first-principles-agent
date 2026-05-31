#!/usr/bin/env python3
"""
阶段33测试：验证序列化器（Serializer类）
"""
import sys
import os
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from first_principles_agent import Serializer

print("=" * 60)
print("阶段33测试：序列化器（Serializer类）")
print("=" * 60)

# 测试1：验证Serializer初始化
print("\n[测试1] 验证Serializer初始化")
try:
    s = Serializer(format_type="json")
    assert s.format_type == "json"
    print("✅ Serializer初始化成功")
except Exception as e:
    print(f"❌ Serializer初始化失败: {e}")

# 测试2：验证JSON序列化
print("\n[测试2] 验证JSON序列化")
try:
    s = Serializer("json")
    data = {"name": "test", "value": 42, "active": True}
    serialized = s.serialize(data)
    assert isinstance(serialized, str)
    assert "test" in serialized
    print("✅ JSON序列化正常")
except Exception as e:
    print(f"❌ JSON序列化失败: {e}")

# 测试3：验证JSON反序列化
print("\n[测试3] 验证JSON反序列化")
try:
    s = Serializer("json")
    data = {"name": "test", "value": 42}
    serialized = s.serialize(data)
    deserialized = s.deserialize(serialized)
    assert deserialized == data
    print("✅ JSON反序列化正常")
except Exception as e:
    print(f"❌ JSON反序列化失败: {e}")

# 测试4：验证嵌套数据结构
print("\n[测试4] 验证嵌套数据结构")
try:
    s = Serializer("json")
    data = {"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}], "count": 2}
    serialized = s.serialize(data)
    deserialized = s.deserialize(serialized)
    assert deserialized["count"] == 2
    assert len(deserialized["users"]) == 2
    print("✅ 嵌套数据结构正常")
except Exception as e:
    print(f"❌ 嵌套数据结构测试失败: {e}")

# 测试5：验证datetime序列化
print("\n[测试5] 验证datetime序列化")
try:
    s = Serializer("json")
    from datetime import datetime
    data = {"created": datetime(2024, 1, 1, 12, 0, 0)}
    serialized = s.serialize(data)
    assert "2024-01-01" in serialized
    print("✅ datetime序列化正常")
except Exception as e:
    print(f"❌ datetime序列化失败: {e}")

# 测试6：验证set序列化
print("\n[测试6] 验证set序列化")
try:
    s = Serializer("json")
    data = {"tags": {"a", "b", "c"}}
    serialized = s.serialize(data)
    deserialized = s.deserialize(serialized)
    assert isinstance(deserialized["tags"], list)
    assert set(deserialized["tags"]) == {"a", "b", "c"}
    print("✅ set序列化正常")
except Exception as e:
    print(f"❌ set序列化失败: {e}")

# 测试7：验证文件保存和加载
print("\n[测试7] 验证文件保存和加载")
try:
    s = Serializer("json")
    data = {"key": "value", "number": 123}
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_path = f.name
    s.save_to_file(data, temp_path)
    loaded = s.load_from_file(temp_path)
    assert loaded == data
    os.remove(temp_path)
    print("✅ 文件保存和加载正常")
except Exception as e:
    print(f"❌ 文件保存和加载测试失败: {e}")

# 测试8：验证bytes格式
print("\n[测试8] 验证bytes格式")
try:
    s = Serializer("bytes")
    data = "hello world"
    serialized = s.serialize(data)
    assert isinstance(serialized, bytes)
    deserialized = s.deserialize(serialized)
    assert deserialized == data
    print("✅ bytes格式正常")
except Exception as e:
    print(f"❌ bytes格式测试失败: {e}")

# 测试9：验证自定义规则
print("\n[测试9] 验证自定义规则")
try:
    s = Serializer("json")
    s.add_custom_rule("custom", lambda x: str(x), lambda x: x)
    assert "custom" in s.custom_rules
    print("✅ 自定义规则正常")
except Exception as e:
    print(f"❌ 自定义规则测试失败: {e}")

# 测试10：验证空数据
print("\n[测试10] 验证空数据")
try:
    s = Serializer("json")
    assert s.serialize({}) == "{}"
    assert s.deserialize("{}") == {}
    assert s.serialize([]) == "[]"
    assert s.deserialize("[]") == []
    print("✅ 空数据正常")
except Exception as e:
    print(f"❌ 空数据测试失败: {e}")

# 测试11：验证列表序列化
print("\n[测试11] 验证列表序列化")
try:
    s = Serializer("json")
    data = [1, 2, 3, "a", "b", True]
    serialized = s.serialize(data)
    deserialized = s.deserialize(serialized)
    assert deserialized == data
    print("✅ 列表序列化正常")
except Exception as e:
    print(f"❌ 列表序列化失败: {e}")

# 测试12：验证字符串反序列化bytes
print("\n[测试12] 验证字符串反序列化bytes")
try:
    s = Serializer("json")
    data = b'{"key": "value"}'
    deserialized = s.deserialize(data)
    assert deserialized == {"key": "value"}
    print("✅ bytes反序列化正常")
except Exception as e:
    print(f"❌ bytes反序列化失败: {e}")

print("\n" + "=" * 60)
print("阶段33测试完成！")
print("=" * 60)
