#!/usr/bin/env python3
"""
阶段37测试：验证安全随机数生成器（SecureRandom类）
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from first_principles_agent import SecureRandom

print("=" * 60)
print("阶段37测试：安全随机数生成器（SecureRandom类）")
print("=" * 60)

# 测试1：验证SecureRandom初始化
print("\n[测试1] 验证SecureRandom初始化")
try:
    sr = SecureRandom()
    assert sr._rng is not None
    print("✅ SecureRandom初始化成功")
except Exception as e:
    print(f"❌ SecureRandom初始化失败: {e}")

# 测试2：验证random方法
print("\n[测试2] 验证random方法")
try:
    sr = SecureRandom()
    r1 = sr.random()
    r2 = sr.random()
    assert 0 <= r1 < 1
    assert 0 <= r2 < 1
    assert r1 != r2
    print(f"✅ random正常: {r1:.4f}, {r2:.4f}")
except Exception as e:
    print(f"❌ random测试失败: {e}")

# 测试3：验证randint方法
print("\n[测试3] 验证randint方法")
try:
    sr = SecureRandom()
    for _ in range(10):
        r = sr.randint(1, 100)
        assert 1 <= r <= 100
    print("✅ randint正常")
except Exception as e:
    print(f"❌ randint测试失败: {e}")

# 测试4：验证choice方法
print("\n[测试4] 验证choice方法")
try:
    sr = SecureRandom()
    seq = ["a", "b", "c", "d", "e"]
    result = sr.choice(seq)
    assert result in seq
    print(f"✅ choice正常: 选中 {result}")
except Exception as e:
    print(f"❌ choice测试失败: {e}")

# 测试5：验证choices方法
print("\n[测试5] 验证choices方法")
try:
    sr = SecureRandom()
    seq = [1, 2, 3, 4, 5]
    result = sr.choices(seq, k=3)
    assert len(result) == 3
    assert all(x in seq for x in result)
    print(f"✅ choices正常: {result}")
except Exception as e:
    print(f"❌ choices测试失败: {e}")

# 测试6：验证shuffle方法
print("\n[测试6] 验证shuffle方法")
try:
    sr = SecureRandom()
    seq = [1, 2, 3, 4, 5]
    shuffled = sr.shuffle(seq.copy())
    assert len(shuffled) == 5
    assert set(shuffled) == {1, 2, 3, 4, 5}
    print(f"✅ shuffle正常: {shuffled}")
except Exception as e:
    print(f"❌ shuffle测试失败: {e}")

# 测试7：验证uniform方法
print("\n[测试7] 验证uniform方法")
try:
    sr = SecureRandom()
    r = sr.uniform(10, 20)
    assert 10 <= r <= 20
    print(f"✅ uniform正常: {r:.4f}")
except Exception as e:
    print(f"❌ uniform测试失败: {e}")

# 测试8：验证gauss方法
print("\n[测试8] 验证gauss方法")
try:
    sr = SecureRandom()
    r = sr.gauss(0, 1)
    assert isinstance(r, float)
    print(f"✅ gauss正常: {r:.4f}")
except Exception as e:
    print(f"❌ gauss测试失败: {e}")

# 测试9：验证bytes方法
print("\n[测试9] 验证bytes方法")
try:
    sr = SecureRandom()
    b = sr.bytes(16)
    assert isinstance(b, bytes)
    assert len(b) == 16
    print(f"✅ bytes正常: {b.hex()[:16]}...")
except Exception as e:
    print(f"❌ bytes测试失败: {e}")

# 测试10：验证hex方法
print("\n[测试10] 验证hex方法")
try:
    sr = SecureRandom()
    h = sr.hex(8)
    assert isinstance(h, str)
    assert len(h) == 16
    print(f"✅ hex正常: {h}")
except Exception as e:
    print(f"❌ hex测试失败: {e}")

# 测试11：验证token方法
print("\n[测试11] 验证token方法")
try:
    sr = SecureRandom()
    t1 = sr.token(16)
    t2 = sr.token(16)
    assert len(t1) == 16
    assert len(t2) == 16
    assert t1 != t2
    print(f"✅ token正常: {t1}")
except Exception as e:
    print(f"❌ token测试失败: {e}")

# 测试12：验证密码学安全
print("\n[测试12] 验证密码学安全")
try:
    sr = SecureRandom()
    tokens = [sr.token(32) for _ in range(100)]
    assert len(set(tokens)) == 100
    print("✅ 密码学安全正常（100个token全部唯一）")
except Exception as e:
    print(f"❌ 密码学安全测试失败: {e}")

print("\n" + "=" * 60)
print("阶段37测试完成！")
print("=" * 60)
