#!/usr/bin/env python3
"""
阶段38测试：验证UUID生成器（UUIDGenerator类）
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from first_principles_agent import UUIDGenerator

print("=" * 60)
print("阶段38测试：UUID生成器（UUIDGenerator类）")
print("=" * 60)

# 测试1：验证v1生成
print("\n[测试1] 验证v1生成")
try:
    u1 = UUIDGenerator.v1()
    u2 = UUIDGenerator.v1()
    assert UUIDGenerator.is_valid(u1)
    assert UUIDGenerator.is_valid(u2)
    assert u1 != u2
    print(f"✅ v1生成正常: {u1}")
except Exception as e:
    print(f"❌ v1生成失败: {e}")

# 测试2：验证v4生成
print("\n[测试2] 验证v4生成")
try:
    u1 = UUIDGenerator.v4()
    u2 = UUIDGenerator.v4()
    assert UUIDGenerator.is_valid(u1)
    assert UUIDGenerator.is_valid(u2)
    assert u1 != u2
    print(f"✅ v4生成正常: {u1}")
except Exception as e:
    print(f"❌ v4生成失败: {e}")

# 测试3：验证v5生成
print("\n[测试3] 验证v5生成")
try:
    ns = "6ba7b810-9dad-11d1-80b4-00c04fd430c8"
    u1 = UUIDGenerator.v5(ns, "name1")
    u2 = UUIDGenerator.v5(ns, "name1")
    u3 = UUIDGenerator.v5(ns, "name2")
    assert UUIDGenerator.is_valid(u1)
    assert u1 == u2
    assert u1 != u3
    print(f"✅ v5生成正常: {u1}")
except Exception as e:
    print(f"❌ v5生成失败: {e}")

# 测试4：验证自定义命名空间
print("\n[测试4] 验证自定义命名空间")
try:
    ns1 = UUIDGenerator.custom_namespace("example.com")
    ns2 = UUIDGenerator.custom_namespace("example.com")
    assert UUIDGenerator.is_valid(ns1)
    assert ns1 == ns2
    print(f"✅ 自定义命名空间正常: {ns1}")
except Exception as e:
    print(f"❌ 自定义命名空间测试失败: {e}")

# 测试5：验证is_valid
print("\n[测试5] 验证is_valid")
try:
    assert UUIDGenerator.is_valid("550e8400-e29b-41d4-a716-446655440000") is True
    assert UUIDGenerator.is_valid("not-a-uuid") is False
    assert UUIDGenerator.is_valid("") is False
    print("✅ is_valid正常")
except Exception as e:
    print(f"❌ is_valid测试失败: {e}")

# 测试6：验证parse
print("\n[测试6] 验证parse")
try:
    parsed = UUIDGenerator.parse("550e8400e29b41d4a716446655440000")
    assert parsed is not None
    assert UUIDGenerator.is_valid(parsed)
    invalid = UUIDGenerator.parse("invalid")
    assert invalid is None
    print(f"✅ parse正常: {parsed}")
except Exception as e:
    print(f"❌ parse测试失败: {e}")

# 测试7：验证v4唯一性
print("\n[测试7] 验证v4唯一性")
try:
    uuids = [UUIDGenerator.v4() for _ in range(1000)]
    assert len(set(uuids)) == 1000
    print("✅ v4唯一性正常（1000个UUID全部唯一）")
except Exception as e:
    print(f"❌ v4唯一性测试失败: {e}")

# 测试8：验证v5确定性
print("\n[测试8] 验证v5确定性")
try:
    ns = UUIDGenerator.custom_namespace("test.com")
    uuids = [UUIDGenerator.v5(ns, "same") for _ in range(10)]
    assert len(set(uuids)) == 1
    print("✅ v5确定性正常（相同输入产生相同UUID）")
except Exception as e:
    print(f"❌ v5确定性测试失败: {e}")

# 测试9：验证UUID格式
print("\n[测试9] 验证UUID格式")
try:
    u = UUIDGenerator.v4()
    parts = u.split("-")
    assert len(parts) == 5
    assert len(parts[0]) == 8
    assert len(parts[1]) == 4
    assert len(parts[2]) == 4
    assert len(parts[3]) == 4
    assert len(parts[4]) == 12
    print("✅ UUID格式正常")
except Exception as e:
    print(f"❌ UUID格式测试失败: {e}")

# 测试10：验证集成到节点ID
print("\n[测试10] 验证集成到节点ID概念")
try:
    node_id = f"node_{UUIDGenerator.v4()}"
    assert len(node_id) > 5
    assert UUIDGenerator.is_valid(node_id.replace("node_", ""))
    print(f"✅ 节点ID集成正常: {node_id[:30]}...")
except Exception as e:
    print(f"❌ 节点ID集成测试失败: {e}")

# 测试11：验证不同命名空间不同结果
print("\n[测试11] 验证不同命名空间不同结果")
try:
    ns1 = UUIDGenerator.custom_namespace("a.com")
    ns2 = UUIDGenerator.custom_namespace("b.com")
    u1 = UUIDGenerator.v5(ns1, "name")
    u2 = UUIDGenerator.v5(ns2, "name")
    assert u1 != u2
    print("✅ 不同命名空间不同结果正常")
except Exception as e:
    print(f"❌ 不同命名空间测试失败: {e}")

# 测试12：验证v1包含时间信息
print("\n[测试12] 验证v1包含时间信息")
try:
    import time
    u1 = UUIDGenerator.v1()
    time.sleep(0.01)
    u2 = UUIDGenerator.v1()
    assert u1 != u2
    assert UUIDGenerator.is_valid(u1)
    assert UUIDGenerator.is_valid(u2)
    print("✅ v1时间信息正常")
except Exception as e:
    print(f"❌ v1时间信息测试失败: {e}")

print("\n" + "=" * 60)
print("阶段38测试完成！")
print("=" * 60)
