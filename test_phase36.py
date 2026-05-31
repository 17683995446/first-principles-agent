#!/usr/bin/env python3
"""
阶段36测试：验证哈希器（Hasher类）
"""
import sys
import os
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from first_principles_agent import Hasher

print("=" * 60)
print("阶段36测试：哈希器（Hasher类）")
print("=" * 60)

# 测试1：验证Hasher初始化
print("\n[测试1] 验证Hasher初始化")
try:
    h = Hasher(algorithm="sha256")
    assert h.algorithm == "sha256"
    print("✅ Hasher初始化成功")
except Exception as e:
    print(f"❌ Hasher初始化失败: {e}")

# 测试2：验证字符串哈希
print("\n[测试2] 验证字符串哈希")
try:
    h = Hasher("sha256")
    hash1 = h.hash("hello")
    hash2 = h.hash("hello")
    assert isinstance(hash1, str)
    assert len(hash1) == 64
    assert hash1 == hash2
    print(f"✅ 字符串哈希正常: {hash1[:16]}...")
except Exception as e:
    print(f"❌ 字符串哈希失败: {e}")

# 测试3：验证不同输入不同哈希
print("\n[测试3] 验证不同输入不同哈希")
try:
    h = Hasher("sha256")
    hash1 = h.hash("hello")
    hash2 = h.hash("world")
    assert hash1 != hash2
    print("✅ 不同输入不同哈希正常")
except Exception as e:
    print(f"❌ 不同输入测试失败: {e}")

# 测试4：验证bytes哈希
print("\n[测试4] 验证bytes哈希")
try:
    h = Hasher("sha256")
    hash1 = h.hash(b"binary data")
    hash2 = h.hash("binary data")
    assert hash1 == hash2
    print("✅ bytes哈希正常")
except Exception as e:
    print(f"❌ bytes哈希失败: {e}")

# 测试5：验证md5算法
print("\n[测试5] 验证md5算法")
try:
    h = Hasher("md5")
    result = h.hash("test")
    assert len(result) == 32
    print(f"✅ md5算法正常: {result[:16]}...")
except Exception as e:
    print(f"❌ md5算法失败: {e}")

# 测试6：验证sha1算法
print("\n[测试6] 验证sha1算法")
try:
    h = Hasher("sha1")
    result = h.hash("test")
    assert len(result) == 40
    print(f"✅ sha1算法正常: {result[:16]}...")
except Exception as e:
    print(f"❌ sha1算法失败: {e}")

# 测试7：验证sha512算法
print("\n[测试7] 验证sha512算法")
try:
    h = Hasher("sha512")
    result = h.hash("test")
    assert len(result) == 128
    print(f"✅ sha512算法正常: {result[:16]}...")
except Exception as e:
    print(f"❌ sha512算法失败: {e}")

# 测试8：验证文件哈希
print("\n[测试8] 验证文件哈希")
try:
    h = Hasher("sha256")
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as f:
        f.write(b"File content for hashing")
        path = f.name
    hash1 = h.hash_file(path)
    hash2 = h.hash_file(path)
    assert isinstance(hash1, str)
    assert hash1 == hash2
    os.remove(path)
    print(f"✅ 文件哈希正常: {hash1[:16]}...")
except Exception as e:
    print(f"❌ 文件哈希失败: {e}")

# 测试9：验证verify
print("\n[测试9] 验证verify")
try:
    h = Hasher("sha256")
    data = "verify me"
    hash_val = h.hash(data)
    assert h.verify(data, hash_val) is True
    assert h.verify(data + "x", hash_val) is False
    print("✅ verify正常")
except Exception as e:
    print(f"❌ verify测试失败: {e}")

# 测试10：验证verify_file
print("\n[测试10] 验证verify_file")
try:
    h = Hasher("sha256")
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as f:
        f.write(b"File to verify")
        path = f.name
    hash_val = h.hash_file(path)
    assert h.verify_file(path, hash_val) is True
    assert h.verify_file(path, hash_val + "x") is False
    os.remove(path)
    print("✅ verify_file正常")
except Exception as e:
    print(f"❌ verify_file测试失败: {e}")

# 测试11：验证checksum切换算法
print("\n[测试11] 验证checksum切换算法")
try:
    h = Hasher("sha256")
    data = "test"
    md5_hash = h.checksum(data, "md5")
    sha1_hash = h.checksum(data, "sha1")
    assert len(md5_hash) == 32
    assert len(sha1_hash) == 40
    assert h.algorithm == "sha256"
    print("✅ checksum切换算法正常")
except Exception as e:
    print(f"❌ checksum测试失败: {e}")

# 测试12：验证不支持的算法
print("\n[测试12] 验证不支持的算法")
try:
    try:
        h = Hasher("unsupported")
        print("❌ 应该抛出异常")
    except ValueError as e:
        assert "不支持" in str(e)
        print("✅ 不支持的算法正确抛出异常")
except Exception as e:
    print(f"❌ 不支持的算法测试失败: {e}")

print("\n" + "=" * 60)
print("阶段36测试完成！")
print("=" * 60)
