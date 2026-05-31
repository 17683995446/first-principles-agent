#!/usr/bin/env python3
"""
阶段41测试：验证数学工具（MathUtils类）
"""
import sys
import os
import math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from first_principles_agent import MathUtils

print("=" * 60)
print("阶段41测试：数学工具（MathUtils类）")
print("=" * 60)

# 测试1：验证mean
print("\n[测试1] 验证mean")
try:
    assert MathUtils.mean([1, 2, 3, 4, 5]) == 3
    assert MathUtils.mean([]) == 0
    print("✅ mean正常")
except Exception as e:
    print(f"❌ mean测试失败: {e}")

# 测试2：验证median
print("\n[测试2] 验证median")
try:
    assert MathUtils.median([1, 2, 3, 4, 5]) == 3
    assert MathUtils.median([1, 2, 3, 4]) == 2.5
    print("✅ median正常")
except Exception as e:
    print(f"❌ median测试失败: {e}")

# 测试3：验证stdev
print("\n[测试3] 验证stdev")
try:
    result = MathUtils.stdev([1, 2, 3, 4, 5])
    assert result > 1.4 and result < 1.6
    assert MathUtils.stdev([1]) == 0
    print(f"✅ stdev正常: {result:.4f}")
except Exception as e:
    print(f"❌ stdev测试失败: {e}")

# 测试4：验证variance
print("\n[测试4] 验证variance")
try:
    result = MathUtils.variance([1, 2, 3, 4, 5])
    assert result > 2.4 and result < 2.6
    print(f"✅ variance正常: {result:.4f}")
except Exception as e:
    print(f"❌ variance测试失败: {e}")

# 测试5：验证max/min/sum
print("\n[测试5] 验证max/min/sum")
try:
    assert MathUtils.max([1, 5, 3]) == 5
    assert MathUtils.min([1, 5, 3]) == 1
    assert MathUtils.sum([1, 2, 3]) == 6
    print("✅ max/min/sum正常")
except Exception as e:
    print(f"❌ max/min/sum测试失败: {e}")

# 测试6：验证normalize
print("\n[测试6] 验证normalize")
try:
    result = MathUtils.normalize([10, 20, 30])
    assert result[0] == 0.0
    assert result[-1] == 1.0
    assert len(result) == 3
    print(f"✅ normalize正常: {result}")
except Exception as e:
    print(f"❌ normalize测试失败: {e}")

# 测试7：验证clamp
print("\n[测试7] 验证clamp")
try:
    assert MathUtils.clamp(5, 0, 10) == 5
    assert MathUtils.clamp(-5, 0, 10) == 0
    assert MathUtils.clamp(15, 0, 10) == 10
    print("✅ clamp正常")
except Exception as e:
    print(f"❌ clamp测试失败: {e}")

# 测试8：验证lerp
print("\n[测试8] 验证lerp")
try:
    assert MathUtils.lerp(0, 10, 0.5) == 5
    assert MathUtils.lerp(0, 10, 0) == 0
    assert MathUtils.lerp(0, 10, 1) == 10
    print("✅ lerp正常")
except Exception as e:
    print(f"❌ lerp测试失败: {e}")

# 测试9：验证sigmoid
print("\n[测试9] 验证sigmoid")
try:
    assert MathUtils.sigmoid(0) == 0.5
    assert MathUtils.sigmoid(10) > 0.99
    assert MathUtils.sigmoid(-10) < 0.01
    print("✅ sigmoid正常")
except Exception as e:
    print(f"❌ sigmoid测试失败: {e}")

# 测试10：验证softmax
print("\n[测试10] 验证softmax")
try:
    result = MathUtils.softmax([1, 2, 3])
    assert abs(sum(result) - 1.0) < 0.001
    assert len(result) == 3
    assert result[2] > result[1] > result[0]
    print(f"✅ softmax正常: {[round(x, 4) for x in result]}")
except Exception as e:
    print(f"❌ softmax测试失败: {e}")

# 测试11：验证entropy
print("\n[测试11] 验证entropy")
try:
    result = MathUtils.entropy([0.5, 0.5])
    assert result == 1.0
    result2 = MathUtils.entropy([1.0])
    assert result2 == 0.0
    print(f"✅ entropy正常: {result}")
except Exception as e:
    print(f"❌ entropy测试失败: {e}")

# 测试12：验证边界条件
print("\n[测试12] 验证边界条件")
try:
    assert MathUtils.normalize([]) == []
    assert MathUtils.normalize([5, 5, 5]) == [0.0, 0.0, 0.0]
    assert MathUtils.entropy([]) == 0
    print("✅ 边界条件正常")
except Exception as e:
    print(f"❌ 边界条件测试失败: {e}")

print("\n" + "=" * 60)
print("阶段41测试完成！")
print("=" * 60)
