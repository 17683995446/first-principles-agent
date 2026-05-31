#!/usr/bin/env python3
"""
阶段40测试：验证字符串工具（StringUtils类）
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from first_principles_agent import StringUtils

print("=" * 60)
print("阶段40测试：字符串工具（StringUtils类）")
print("=" * 60)

# 测试1：验证is_empty
print("\n[测试1] 验证is_empty")
try:
    assert StringUtils.is_empty("") is True
    assert StringUtils.is_empty("   ") is True
    assert StringUtils.is_empty(None) is True
    assert StringUtils.is_empty("hello") is False
    print("✅ is_empty正常")
except Exception as e:
    print(f"❌ is_empty测试失败: {e}")

# 测试2：验证is_not_empty
print("\n[测试2] 验证is_not_empty")
try:
    assert StringUtils.is_not_empty("hello") is True
    assert StringUtils.is_not_empty("") is False
    print("✅ is_not_empty正常")
except Exception as e:
    print(f"❌ is_not_empty测试失败: {e}")

# 测试3：验证trim
print("\n[测试3] 验证trim")
try:
    assert StringUtils.trim("  hello  ") == "hello"
    assert StringUtils.trim("hello") == "hello"
    print("✅ trim正常")
except Exception as e:
    print(f"❌ trim测试失败: {e}")

# 测试4：验证truncate
print("\n[测试4] 验证truncate")
try:
    assert StringUtils.truncate("hello world", 8) == "hello..."
    assert StringUtils.truncate("hi", 10) == "hi"
    print("✅ truncate正常")
except Exception as e:
    print(f"❌ truncate测试失败: {e}")

# 测试5：验证contains
print("\n[测试5] 验证contains")
try:
    assert StringUtils.contains("hello world", "world") is True
    assert StringUtils.contains("hello world", "xyz") is False
    print("✅ contains正常")
except Exception as e:
    print(f"❌ contains测试失败: {e}")

# 测试6：验证starts_with
print("\n[测试6] 验证starts_with")
try:
    assert StringUtils.starts_with("hello", "he") is True
    assert StringUtils.starts_with("hello", "lo") is False
    print("✅ starts_with正常")
except Exception as e:
    print(f"❌ starts_with测试失败: {e}")

# 测试7：验证ends_with
print("\n[测试7] 验证ends_with")
try:
    assert StringUtils.ends_with("hello", "lo") is True
    assert StringUtils.ends_with("hello", "he") is False
    print("✅ ends_with正常")
except Exception as e:
    print(f"❌ ends_with测试失败: {e}")

# 测试8：验证split
print("\n[测试8] 验证split")
try:
    result = StringUtils.split("a,b,c")
    assert result == ["a", "b", "c"]
    result2 = StringUtils.split("a; b; c", ";")
    assert result2 == ["a", "b", "c"]
    print("✅ split正常")
except Exception as e:
    print(f"❌ split测试失败: {e}")

# 测试9：验证join
print("\n[测试9] 验证join")
try:
    result = StringUtils.join(["a", "b", "c"], "-")
    assert result == "a-b-c"
    print("✅ join正常")
except Exception as e:
    print(f"❌ join测试失败: {e}")

# 测试10：验证to_camel_case
print("\n[测试10] 验证to_camel_case")
try:
    assert StringUtils.to_camel_case("hello_world") == "helloWorld"
    assert StringUtils.to_camel_case("hello-world") == "helloWorld"
    print("✅ to_camel_case正常")
except Exception as e:
    print(f"❌ to_camel_case测试失败: {e}")

# 测试11：验证to_snake_case
print("\n[测试11] 验证to_snake_case")
try:
    assert StringUtils.to_snake_case("helloWorld") == "hello_world"
    assert StringUtils.to_snake_case("HelloWorld") == "hello_world"
    print("✅ to_snake_case正常")
except Exception as e:
    print(f"❌ to_snake_case测试失败: {e}")

# 测试12：验证match和find_all
print("\n[测试12] 验证match和find_all")
try:
    assert StringUtils.match(r"\d+", "123abc") is not None
    assert StringUtils.match(r"[a-z]+", "123abc") is None
    result = StringUtils.find_all(r"\d+", "a1b2c3")
    assert result == ["1", "2", "3"]
    print("✅ match和find_all正常")
except Exception as e:
    print(f"❌ match和find_all测试失败: {e}")

# 测试13：验证replace_all
print("\n[测试13] 验证replace_all")
try:
    result = StringUtils.replace_all(r"\d+", "X", "a1b2c3")
    assert result == "aXbXcX"
    print("✅ replace_all正常")
except Exception as e:
    print(f"❌ replace_all测试失败: {e}")

# 测试14：验证word_count
print("\n[测试14] 验证word_count")
try:
    assert StringUtils.word_count("hello world foo") == 3
    assert StringUtils.word_count("") == 0
    print("✅ word_count正常")
except Exception as e:
    print(f"❌ word_count测试失败: {e}")

# 测试15：验证char_count
print("\n[测试15] 验证char_count")
try:
    assert StringUtils.char_count("hello world", "l") == 3
    assert StringUtils.char_count("hello world", "x") == 0
    print("✅ char_count正常")
except Exception as e:
    print(f"❌ char_count测试失败: {e}")

print("\n" + "=" * 60)
print("阶段40测试完成！")
print("=" * 60)
