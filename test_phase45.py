#!/usr/bin/env python3
"""
阶段45测试：验证进程工具（ProcessUtils类）
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from first_principles_agent import ProcessUtils

print("=" * 60)
print("阶段45测试：进程工具（ProcessUtils类）")
print("=" * 60)

# 测试1：验证run命令
print("\n[测试1] 验证run命令")
try:
    result = ProcessUtils.run("echo hello")
    assert result["returncode"] == 0
    assert "hello" in result["stdout"]
    print("✅ run命令正常")
except Exception as e:
    print(f"❌ run命令测试失败: {e}")

# 测试2：验证run命令shell模式
print("\n[测试2] 验证run命令shell模式")
try:
    result = ProcessUtils.run("echo $HOME", shell=True)
    assert result["returncode"] == 0
    assert len(result["stdout"]) > 0
    print("✅ run命令shell模式正常")
except Exception as e:
    print(f"❌ run命令shell模式测试失败: {e}")

# 测试3：验证run命令超时
print("\n[测试3] 验证run命令超时")
try:
    result = ProcessUtils.run("sleep 5", timeout=0.1)
    assert result["returncode"] == -1
    assert "timeout" in result["stderr"]
    print("✅ run命令超时正常")
except Exception as e:
    print(f"❌ run命令超时测试失败: {e}")

# 测试4：验证get_pid
print("\n[测试4] 验证get_pid")
try:
    pid = ProcessUtils.get_pid()
    assert isinstance(pid, int)
    assert pid > 0
    print(f"✅ get_pid正常: {pid}")
except Exception as e:
    print(f"❌ get_pid测试失败: {e}")

# 测试5：验证get_ppid
print("\n[测试5] 验证get_ppid")
try:
    ppid = ProcessUtils.get_ppid()
    assert isinstance(ppid, int)
    assert ppid > 0
    print(f"✅ get_ppid正常: {ppid}")
except Exception as e:
    print(f"❌ get_ppid测试失败: {e}")

# 测试6：验证cpu_count
print("\n[测试6] 验证cpu_count")
try:
    count = ProcessUtils.cpu_count()
    assert isinstance(count, int)
    assert count >= 1
    print(f"✅ cpu_count正常: {count}")
except Exception as e:
    print(f"❌ cpu_count测试失败: {e}")

# 测试7：验证get_env和set_env
print("\n[测试7] 验证get_env和set_env")
try:
    ProcessUtils.set_env("TEST_VAR_12345", "test_value")
    result = ProcessUtils.get_env("TEST_VAR_12345")
    assert result == "test_value"
    default = ProcessUtils.get_env("NONEXISTENT_VAR_12345", "default")
    assert default == "default"
    print("✅ get_env和set_env正常")
except Exception as e:
    print(f"❌ get_env和set_env测试失败: {e}")

# 测试8：验证run_async
print("\n[测试8] 验证run_async")
try:
    proc = ProcessUtils.run_async("echo async_test")
    stdout, stderr = proc.communicate(timeout=5)
    assert "async_test" in stdout
    print("✅ run_async正常")
except Exception as e:
    print(f"❌ run_async测试失败: {e}")

# 测试9：验证run命令错误返回码
print("\n[测试9] 验证run命令错误返回码")
try:
    result = ProcessUtils.run("false")
    assert result["returncode"] != 0
    print("✅ run命令错误返回码正常")
except Exception as e:
    print(f"❌ run命令错误返回码测试失败: {e}")

# 测试10：验证run命令无效命令
print("\n[测试10] 验证run命令无效命令")
try:
    result = ProcessUtils.run("nonexistent_command_12345")
    assert result["returncode"] == -1
    print("✅ run命令无效命令正常")
except Exception as e:
    print(f"❌ run命令无效命令测试失败: {e}")

# 测试11：验证kill（不实际kill）
print("\n[测试11] 验证kill无效PID")
try:
    result = ProcessUtils.kill(999999, sig=9)
    assert result is False
    print("✅ kill无效PID正常")
except Exception as e:
    print(f"❌ kill测试失败: {e}")

# 测试12：验证run命令stderr
print("\n[测试12] 验证run命令stderr")
try:
    result = ProcessUtils.run("ls /nonexistent_path_12345")
    assert result["stderr"] != "" or result["returncode"] != 0
    print("✅ run命令stderr正常")
except Exception as e:
    print(f"❌ run命令stderr测试失败: {e}")

print("\n" + "=" * 60)
print("阶段45测试完成！")
print("=" * 60)
