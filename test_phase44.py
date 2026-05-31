#!/usr/bin/env python3
"""
阶段44测试：验证网络工具（NetworkUtils类）
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from first_principles_agent import NetworkUtils

print("=" * 60)
print("阶段44测试：网络工具（NetworkUtils类）")
print("=" * 60)

# 测试1：验证parse_url
print("\n[测试1] 验证parse_url")
try:
    result = NetworkUtils.parse_url("https://example.com/path?a=1&b=2#frag")
    assert result["scheme"] == "https"
    assert result["netloc"] == "example.com"
    assert result["path"] == "/path"
    assert result["query"]["a"] == ["1"]
    assert result["fragment"] == "frag"
    print(f"✅ parse_url正常: {result}")
except Exception as e:
    print(f"❌ parse_url测试失败: {e}")

# 测试2：验证build_url
print("\n[测试2] 验证build_url")
try:
    result = NetworkUtils.build_url("https://example.com", {"a": "1", "b": "2"})
    assert "a=1" in result
    assert "b=2" in result
    print(f"✅ build_url正常: {result}")
except Exception as e:
    print(f"❌ build_url测试失败: {e}")

# 测试3：验证is_port_open（本地SSH端口）
print("\n[测试3] 验证is_port_open")
try:
    result = NetworkUtils.is_port_open("127.0.0.1", 22, timeout=1)
    print(f"✅ is_port_open正常: SSH端口22 {'开放' if result else '关闭'}")
except Exception as e:
    print(f"⚠️ is_port_open测试: {e}")

# 测试4：验证is_port_open（关闭端口）
print("\n[测试4] 验证is_port_open（关闭端口）")
try:
    result = NetworkUtils.is_port_open("127.0.0.1", 65432, timeout=1)
    assert result is False
    print("✅ is_port_open关闭端口正常")
except Exception as e:
    print(f"❌ is_port_open测试失败: {e}")

# 测试5：验证get_local_ip
print("\n[测试5] 验证get_local_ip")
try:
    ip = NetworkUtils.get_local_ip()
    assert isinstance(ip, str)
    assert len(ip) > 0
    parts = ip.split(".")
    assert len(parts) == 4
    print(f"✅ get_local_ip正常: {ip}")
except Exception as e:
    print(f"❌ get_local_ip测试失败: {e}")

# 测试6：验证parse_url无query
print("\n[测试6] 验证parse_url无query")
try:
    result = NetworkUtils.parse_url("https://example.com/path")
    assert result["query"] == {}
    print("✅ parse_url无query正常")
except Exception as e:
    print(f"❌ parse_url无query测试失败: {e}")

# 测试7：验证build_url空参数
print("\n[测试7] 验证build_url空参数")
try:
    result = NetworkUtils.build_url("https://example.com", {})
    assert result == "https://example.com"
    print("✅ build_url空参数正常")
except Exception as e:
    print(f"❌ build_url空参数测试失败: {e}")

# 测试8：验证parse_url复杂query
print("\n[测试8] 验证parse_url复杂query")
try:
    result = NetworkUtils.parse_url("https://example.com?arr=1&arr=2&key=val")
    assert result["query"]["arr"] == ["1", "2"]
    assert result["query"]["key"] == ["val"]
    print("✅ parse_url复杂query正常")
except Exception as e:
    print(f"❌ parse_url复杂query测试失败: {e}")

# 测试9：验证is_port_open无效主机
print("\n[测试9] 验证is_port_open无效主机")
try:
    result = NetworkUtils.is_port_open("256.256.256.256", 80, timeout=1)
    assert result is False
    print("✅ is_port_open无效主机正常")
except Exception as e:
    print(f"❌ is_port_open无效主机测试失败: {e}")

# 测试10：验证URL解析http
print("\n[测试10] 验证URL解析http")
try:
    result = NetworkUtils.parse_url("http://localhost:8080/api")
    assert result["scheme"] == "http"
    assert result["netloc"] == "localhost:8080"
    assert result["path"] == "/api"
    print("✅ URL解析http正常")
except Exception as e:
    print(f"❌ URL解析http测试失败: {e}")

# 测试11：验证build_url列表参数
print("\n[测试11] 验证build_url列表参数")
try:
    result = NetworkUtils.build_url("https://example.com", {"tag": ["a", "b"]})
    assert "tag=a" in result
    assert "tag=b" in result
    print(f"✅ build_url列表参数正常: {result}")
except Exception as e:
    print(f"❌ build_url列表参数测试失败: {e}")

# 测试12：验证get_local_ip返回有效IP
print("\n[测试12] 验证get_local_ip返回有效IP")
try:
    ip = NetworkUtils.get_local_ip()
    assert ip != ""
    assert all(0 <= int(p) <= 255 for p in ip.split("."))
    print(f"✅ get_local_ip返回有效IP: {ip}")
except Exception as e:
    print(f"❌ get_local_ip测试失败: {e}")

print("\n" + "=" * 60)
print("阶段44测试完成！")
print("=" * 60)
