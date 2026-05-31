#!/usr/bin/env python3
"""
阶段39测试：验证时间工具（TimeUtils类）
"""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from first_principles_agent import TimeUtils
from datetime import datetime, timezone, timedelta

print("=" * 60)
print("阶段39测试：时间工具（TimeUtils类）")
print("=" * 60)

# 测试1：验证now方法
print("\n[测试1] 验证now方法")
try:
    now = TimeUtils.now()
    assert isinstance(now, datetime)
    print(f"✅ now正常: {now}")
except Exception as e:
    print(f"❌ now测试失败: {e}")

# 测试2：验证now_utc方法
print("\n[测试2] 验证now_utc方法")
try:
    utc = TimeUtils.now_utc()
    assert isinstance(utc, datetime)
    assert utc.tzinfo is not None
    print(f"✅ now_utc正常: {utc}")
except Exception as e:
    print(f"❌ now_utc测试失败: {e}")

# 测试3：验证format方法
print("\n[测试3] 验证format方法")
try:
    dt = datetime(2024, 1, 15, 10, 30, 0)
    formatted = TimeUtils.format(dt, "%Y-%m-%d %H:%M:%S")
    assert formatted == "2024-01-15 10:30:00"
    print(f"✅ format正常: {formatted}")
except Exception as e:
    print(f"❌ format测试失败: {e}")

# 测试4：验证parse方法
print("\n[测试4] 验证parse方法")
try:
    dt = TimeUtils.parse("2024-01-15 10:30:00", "%Y-%m-%d %H:%M:%S")
    assert isinstance(dt, datetime)
    assert dt.year == 2024
    assert dt.month == 1
    assert dt.day == 15
    print(f"✅ parse正常: {dt}")
except Exception as e:
    print(f"❌ parse测试失败: {e}")

# 测试5：验证timestamp方法
print("\n[测试5] 验证timestamp方法")
try:
    ts = TimeUtils.timestamp()
    assert isinstance(ts, float)
    assert ts > 0
    print(f"✅ timestamp正常: {ts}")
except Exception as e:
    print(f"❌ timestamp测试失败: {e}")

# 测试6：验证timestamp_ms方法
print("\n[测试6] 验证timestamp_ms方法")
try:
    ts = TimeUtils.timestamp_ms()
    assert isinstance(ts, int)
    assert ts > 0
    print(f"✅ timestamp_ms正常: {ts}")
except Exception as e:
    print(f"❌ timestamp_ms测试失败: {e}")

# 测试7：验证to_utc方法
print("\n[测试7] 验证to_utc方法")
try:
    dt = datetime(2024, 1, 1, 12, 0, 0)
    utc = TimeUtils.to_utc(dt)
    assert utc.tzinfo is not None
    print(f"✅ to_utc正常: {utc}")
except Exception as e:
    print(f"❌ to_utc测试失败: {e}")

# 测试8：验证add_seconds方法
print("\n[测试8] 验证add_seconds方法")
try:
    dt = datetime(2024, 1, 1, 12, 0, 0)
    result = TimeUtils.add_seconds(dt, 30)
    assert result.minute == 0
    assert result.second == 30
    print(f"✅ add_seconds正常: {result}")
except Exception as e:
    print(f"❌ add_seconds测试失败: {e}")

# 测试9：验证add_days方法
print("\n[测试9] 验证add_days方法")
try:
    dt = datetime(2024, 1, 1, 12, 0, 0)
    result = TimeUtils.add_days(dt, 5)
    assert result.day == 6
    print(f"✅ add_days正常: {result}")
except Exception as e:
    print(f"❌ add_days测试失败: {e}")

# 测试10：验证sleep方法
print("\n[测试10] 验证sleep方法")
try:
    start = time.time()
    TimeUtils.sleep(0.1)
    elapsed = time.time() - start
    assert elapsed >= 0.09
    print(f"✅ sleep正常: {elapsed:.3f}s")
except Exception as e:
    print(f"❌ sleep测试失败: {e}")

# 测试11：验证timer方法
print("\n[测试11] 验证timer方法")
try:
    t = TimeUtils.timer("test")
    assert t["name"] == "test"
    assert "start" in t
    time.sleep(0.05)
    elapsed = TimeUtils.timer_elapsed(t)
    assert elapsed >= 0.04
    print(f"✅ timer正常: {elapsed:.3f}s")
except Exception as e:
    print(f"❌ timer测试失败: {e}")

# 测试12：验证isoformat方法
print("\n[测试12] 验证isoformat方法")
try:
    dt = datetime(2024, 1, 15, 10, 30, 0)
    iso = TimeUtils.isoformat(dt)
    assert "2024-01-15" in iso
    assert "10:30:00" in iso
    now_iso = TimeUtils.isoformat()
    assert "T" in now_iso or "-" in now_iso
    print(f"✅ isoformat正常: {iso}")
except Exception as e:
    print(f"❌ isoformat测试失败: {e}")

print("\n" + "=" * 60)
print("阶段39测试完成！")
print("=" * 60)
