#!/usr/bin/env python3
"""
阶段32测试：验证限流器（RateLimiter类）
"""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from first_principles_agent import RateLimiter, APIWrapper, FirstPrincipleEternalAgent

print("=" * 60)
print("阶段32测试：限流器（RateLimiter类）")
print("=" * 60)

# 测试1：验证RateLimiter初始化
print("\n[测试1] 验证RateLimiter初始化")
try:
    rl = RateLimiter(rate=5, capacity=10, strategy="token_bucket")
    assert rl.rate == 5
    assert rl.capacity == 10
    assert rl.strategy == "token_bucket"
    assert rl.tokens == 10
    print("✅ RateLimiter初始化成功")
except Exception as e:
    print(f"❌ RateLimiter初始化失败: {e}")

# 测试2：验证令牌桶允许请求
print("\n[测试2] 验证令牌桶允许请求")
try:
    rl = RateLimiter(rate=10, capacity=5)
    for i in range(5):
        assert rl.allow() is True, f"第{i+1}次请求应该被允许"
    print("✅ 令牌桶允许请求正常")
except Exception as e:
    print(f"❌ 令牌桶允许请求失败: {e}")

# 测试3：验证令牌桶拒绝请求
print("\n[测试3] 验证令牌桶拒绝请求")
try:
    rl = RateLimiter(rate=10, capacity=2)
    assert rl.allow() is True
    assert rl.allow() is True
    assert rl.allow() is False
    print("✅ 令牌桶拒绝请求正常")
except Exception as e:
    print(f"❌ 令牌桶拒绝请求失败: {e}")

# 测试4：验证令牌恢复
print("\n[测试4] 验证令牌恢复")
try:
    rl = RateLimiter(rate=10, capacity=1)
    assert rl.allow() is True
    assert rl.allow() is False
    time.sleep(0.15)
    assert rl.allow() is True
    print("✅ 令牌恢复正常")
except Exception as e:
    print(f"❌ 令牌恢复测试失败: {e}")

# 测试5：验证固定窗口策略
print("\n[测试5] 验证固定窗口策略")
try:
    rl = RateLimiter(rate=1, capacity=2, strategy="fixed_window")
    assert rl.allow() is True
    assert rl.allow() is True
    assert rl.allow() is False
    print("✅ 固定窗口策略正常")
except Exception as e:
    print(f"❌ 固定窗口策略测试失败: {e}")

# 测试6：验证滑动窗口策略
print("\n[测试6] 验证滑动窗口策略")
try:
    rl = RateLimiter(rate=1, capacity=2, strategy="sliding_window")
    assert rl.allow() is True
    assert rl.allow() is True
    assert rl.allow() is False
    print("✅ 滑动窗口策略正常")
except Exception as e:
    print(f"❌ 滑动窗口策略测试失败: {e}")

# 测试7：验证stats统计
print("\n[测试7] 验证stats统计")
try:
    rl = RateLimiter(rate=10, capacity=5)
    rl.allow()
    rl.allow()
    rl.allow()
    stats = rl.get_stats()
    assert stats["rate"] == 10
    assert stats["capacity"] == 5
    assert stats["requests"] == 3
    print(f"✅ stats统计正常: {stats}")
except Exception as e:
    print(f"❌ stats统计测试失败: {e}")

# 测试8：验证拒绝计数
print("\n[测试8] 验证拒绝计数")
try:
    rl = RateLimiter(rate=10, capacity=1)
    rl.allow()
    rl.allow()
    rl.allow()
    stats = rl.get_stats()
    assert stats["rejected"] == 2
    print("✅ 拒绝计数正常")
except Exception as e:
    print(f"❌ 拒绝计数测试失败: {e}")

# 测试9：验证集成到APIWrapper
print("\n[测试9] 验证集成到APIWrapper")
try:
    agent = FirstPrincipleEternalAgent()
    api = APIWrapper(agent)
    assert hasattr(api, 'rate_limiter')
    assert isinstance(api.rate_limiter, RateLimiter)
    print("✅ APIWrapper集成RateLimiter成功")
except Exception as e:
    print(f"❌ APIWrapper集成测试失败: {e}")

# 测试10：验证限流触发
print("\n[测试10] 验证限流触发")
try:
    agent = FirstPrincipleEternalAgent()
    api = APIWrapper(agent)
    api.rate_limiter = RateLimiter(rate=1000, capacity=0)
    result = api.handle_request("GET", "/status")
    assert result.get("status") == 429
    assert "Rate limit" in result.get("error", "")
    print("✅ 限流触发正常")
except Exception as e:
    print(f"❌ 限流触发测试失败: {e}")

# 测试11：验证正常请求不受限流影响
print("\n[测试11] 验证正常请求不受限流影响")
try:
    agent = FirstPrincipleEternalAgent()
    api = APIWrapper(agent)
    result = api.handle_request("GET", "/status")
    assert result.get("status") == 200
    print("✅ 正常请求正常")
except Exception as e:
    print(f"❌ 正常请求测试失败: {e}")

# 测试12：验证多token消耗
print("\n[测试12] 验证多token消耗")
try:
    rl = RateLimiter(rate=10, capacity=5)
    assert rl.allow(tokens=3) is True
    assert rl.allow(tokens=3) is False
    assert rl.allow(tokens=1) is True
    print("✅ 多token消耗正常")
except Exception as e:
    print(f"❌ 多token消耗测试失败: {e}")

print("\n" + "=" * 60)
print("阶段32测试完成！")
print("=" * 60)
