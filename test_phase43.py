#!/usr/bin/env python3
"""
阶段43测试：验证文件工具（FileUtils类）
"""
import sys
import os
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from first_principles_agent import FileUtils

print("=" * 60)
print("阶段43测试：文件工具（FileUtils类）")
print("=" * 60)

# 测试1：验证exists
print("\n[测试1] 验证exists")
try:
    assert FileUtils.exists("/tmp") is True
    assert FileUtils.exists("/nonexistent_path_12345") is False
    print("✅ exists正常")
except Exception as e:
    print(f"❌ exists测试失败: {e}")

# 测试2：验证is_file和is_dir
print("\n[测试2] 验证is_file和is_dir")
try:
    assert FileUtils.is_dir("/tmp") is True
    assert FileUtils.is_file("/tmp") is False
    print("✅ is_file和is_dir正常")
except Exception as e:
    print(f"❌ is_file和is_dir测试失败: {e}")

# 测试3：验证write和read
print("\n[测试3] 验证write和read")
try:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as f:
        path = f.name
    FileUtils.write(path, "hello world")
    content = FileUtils.read(path)
    assert content == "hello world"
    os.remove(path)
    print("✅ write和read正常")
except Exception as e:
    print(f"❌ write和read测试失败: {e}")

# 测试4：验证ensure_dir
print("\n[测试4] 验证ensure_dir")
try:
    test_dir = "/tmp/test_fileutils_dir_12345"
    if os.path.exists(test_dir):
        os.rmdir(test_dir)
    result = FileUtils.ensure_dir(test_dir)
    assert result is True
    assert os.path.isdir(test_dir)
    result2 = FileUtils.ensure_dir(test_dir)
    assert result2 is False
    os.rmdir(test_dir)
    print("✅ ensure_dir正常")
except Exception as e:
    print(f"❌ ensure_dir测试失败: {e}")

# 测试5：验证size
print("\n[测试5] 验证size")
try:
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"12345")
        path = f.name
    assert FileUtils.size(path) == 5
    assert FileUtils.size("/nonexistent") == 0
    os.remove(path)
    print("✅ size正常")
except Exception as e:
    print(f"❌ size测试失败: {e}")

# 测试6：验证list_files
print("\n[测试6] 验证list_files")
try:
    test_dir = "/tmp/test_listfiles_12345"
    os.makedirs(test_dir, exist_ok=True)
    open(os.path.join(test_dir, "a.txt"), "w").close()
    open(os.path.join(test_dir, "b.py"), "w").close()
    result = FileUtils.list_files(test_dir, "*.txt")
    assert len(result) == 1
    assert result[0].endswith("a.txt")
    import shutil
    shutil.rmtree(test_dir)
    print("✅ list_files正常")
except Exception as e:
    print(f"❌ list_files测试失败: {e}")

# 测试7：验证copy
print("\n[测试7] 验证copy")
try:
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"copy me")
        src = f.name
    dst = src + ".copy"
    FileUtils.copy(src, dst)
    assert os.path.exists(dst)
    assert FileUtils.read(dst) == "copy me"
    os.remove(src)
    os.remove(dst)
    print("✅ copy正常")
except Exception as e:
    print(f"❌ copy测试失败: {e}")

# 测试8：验证move
print("\n[测试8] 验证move")
try:
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"move me")
        src = f.name
    dst = src + ".moved"
    FileUtils.move(src, dst)
    assert not os.path.exists(src)
    assert os.path.exists(dst)
    os.remove(dst)
    print("✅ move正常")
except Exception as e:
    print(f"❌ move测试失败: {e}")

# 测试9：验证remove
print("\n[测试9] 验证remove")
try:
    with tempfile.NamedTemporaryFile(delete=False) as f:
        path = f.name
    assert os.path.exists(path)
    FileUtils.remove(path)
    assert not os.path.exists(path)
    print("✅ remove正常")
except Exception as e:
    print(f"❌ remove测试失败: {e}")

# 测试10：验证get_mtime
print("\n[测试10] 验证get_mtime")
try:
    with tempfile.NamedTemporaryFile(delete=False) as f:
        path = f.name
    mtime = FileUtils.get_mtime(path)
    assert mtime > 0
    assert FileUtils.get_mtime("/nonexistent") == 0
    os.remove(path)
    print(f"✅ get_mtime正常: {mtime}")
except Exception as e:
    print(f"❌ get_mtime测试失败: {e}")

# 测试11：验证walk
print("\n[测试11] 验证walk")
try:
    test_dir = "/tmp/test_walk_12345"
    os.makedirs(os.path.join(test_dir, "sub"), exist_ok=True)
    open(os.path.join(test_dir, "a.txt"), "w").close()
    open(os.path.join(test_dir, "sub", "b.txt"), "w").close()
    result = FileUtils.walk(test_dir)
    assert len(result) == 2
    import shutil
    shutil.rmtree(test_dir)
    print(f"✅ walk正常: 找到 {len(result)} 个文件")
except Exception as e:
    print(f"❌ walk测试失败: {e}")

# 测试12：验证bytes读写
print("\n[测试12] 验证bytes读写")
try:
    with tempfile.NamedTemporaryFile(delete=False) as f:
        path = f.name
    FileUtils.write(path, b"binary data", mode="wb")
    content = FileUtils.read(path, mode="rb")
    assert content == b"binary data"
    os.remove(path)
    print("✅ bytes读写正常")
except Exception as e:
    print(f"❌ bytes读写测试失败: {e}")

print("\n" + "=" * 60)
print("阶段43测试完成！")
print("=" * 60)
