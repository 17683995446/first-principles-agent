#!/usr/bin/env python3
"""
阶段34测试：验证压缩器（Compressor类）
"""
import sys
import os
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from first_principles_agent import Compressor

print("=" * 60)
print("阶段34测试：压缩器（Compressor类）")
print("=" * 60)

# 测试1：验证Compressor初始化
print("\n[测试1] 验证Compressor初始化")
try:
    c = Compressor(method="gzip", threshold=1024)
    assert c.method == "gzip"
    assert c.threshold == 1024
    print("✅ Compressor初始化成功")
except Exception as e:
    print(f"❌ Compressor初始化失败: {e}")

# 测试2：验证gzip压缩
print("\n[测试2] 验证gzip压缩")
try:
    c = Compressor(method="gzip", threshold=1)
    data = b"Hello World! This is a test string for compression." * 100
    compressed = c.compress(data)
    assert len(compressed) < len(data)
    print(f"✅ gzip压缩正常: {len(data)} -> {len(compressed)} bytes")
except Exception as e:
    print(f"❌ gzip压缩失败: {e}")

# 测试3：验证gzip解压
print("\n[测试3] 验证gzip解压")
try:
    c = Compressor(method="gzip", threshold=1)
    data = b"Hello World! This is a test string for compression." * 100
    compressed = c.compress(data)
    decompressed = c.decompress(compressed)
    assert decompressed == data
    print("✅ gzip解压正常")
except Exception as e:
    print(f"❌ gzip解压失败: {e}")

# 测试4：验证bzip2压缩
print("\n[测试4] 验证bzip2压缩")
try:
    c = Compressor(method="bzip2", threshold=1)
    data = b"Hello World! This is a test string for compression." * 100
    compressed = c.compress(data)
    assert len(compressed) < len(data)
    print(f"✅ bzip2压缩正常: {len(data)} -> {len(compressed)} bytes")
except Exception as e:
    print(f"❌ bzip2压缩失败: {e}")

# 测试5：验证bzip2解压
print("\n[测试5] 验证bzip2解压")
try:
    c = Compressor(method="bzip2", threshold=1)
    data = b"Hello World! This is a test string for compression." * 100
    compressed = c.compress(data)
    decompressed = c.decompress(compressed)
    assert decompressed == data
    print("✅ bzip2解压正常")
except Exception as e:
    print(f"❌ bzip2解压失败: {e}")

# 测试6：验证小文件不压缩
print("\n[测试6] 验证小文件不压缩")
try:
    c = Compressor(method="gzip", threshold=1024)
    data = b"small"
    compressed = c.compress(data)
    assert compressed == data
    print("✅ 小文件不压缩正常")
except Exception as e:
    print(f"❌ 小文件不压缩测试失败: {e}")

# 测试7：验证字符串压缩
print("\n[测试7] 验证字符串压缩")
try:
    c = Compressor(method="gzip", threshold=1)
    data = "Hello World! " * 100
    compressed = c.compress(data)
    assert isinstance(compressed, bytes)
    decompressed = c.decompress(compressed)
    assert decompressed == data.encode("utf-8")
    print("✅ 字符串压缩正常")
except Exception as e:
    print(f"❌ 字符串压缩失败: {e}")

# 测试8：验证文件压缩
print("\n[测试8] 验证文件压缩")
try:
    c = Compressor(method="gzip", threshold=1)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as f:
        f.write(b"Test data for file compression." * 100)
        src_path = f.name
    dst_path = c.compress_file(src_path)
    assert os.path.exists(dst_path)
    assert os.path.getsize(dst_path) < os.path.getsize(src_path)
    os.remove(src_path)
    os.remove(dst_path)
    print("✅ 文件压缩正常")
except Exception as e:
    print(f"❌ 文件压缩测试失败: {e}")

# 测试9：验证文件解压
print("\n[测试9] 验证文件解压")
try:
    c = Compressor(method="gzip", threshold=1)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as f:
        original = b"Test data for file decompression." * 100
        f.write(original)
        src_path = f.name
    compressed_path = c.compress_file(src_path)
    decompressed_path = c.decompress_file(compressed_path)
    with open(decompressed_path, "rb") as f:
        result = f.read()
    assert result == original
    os.remove(src_path)
    os.remove(compressed_path)
    os.remove(decompressed_path)
    print("✅ 文件解压正常")
except Exception as e:
    print(f"❌ 文件解压测试失败: {e}")

# 测试10：验证解压损坏数据
print("\n[测试10] 验证解压损坏数据")
try:
    c = Compressor(method="gzip")
    bad_data = b"not compressed data"
    result = c.decompress(bad_data)
    assert result == bad_data
    print("✅ 解压损坏数据正常（返回原数据）")
except Exception as e:
    print(f"❌ 解压损坏数据测试失败: {e}")

# 测试11：验证bzip2文件压缩
print("\n[测试11] 验证bzip2文件压缩")
try:
    c = Compressor(method="bzip2", threshold=1)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as f:
        f.write(b"Test data for bzip2 compression." * 100)
        src_path = f.name
    dst_path = c.compress_file(src_path)
    assert os.path.exists(dst_path)
    assert dst_path.endswith(".bz2")
    os.remove(src_path)
    os.remove(dst_path)
    print("✅ bzip2文件压缩正常")
except Exception as e:
    print(f"❌ bzip2文件压缩测试失败: {e}")

# 测试12：验证压缩比
print("\n[测试12] 验证压缩比")
try:
    c = Compressor(method="gzip", threshold=1)
    data = b"A" * 10000
    compressed = c.compress(data)
    ratio = len(compressed) / len(data)
    assert ratio < 0.1
    print(f"✅ 压缩比正常: {ratio:.2%}")
except Exception as e:
    print(f"❌ 压缩比测试失败: {e}")

print("\n" + "=" * 60)
print("阶段34测试完成！")
print("=" * 60)
