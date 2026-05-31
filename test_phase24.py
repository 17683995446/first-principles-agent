#!/usr/bin/env python3
"""
阶段24测试：验证单元测试框架
"""
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from test_framework import TestCase, TestRunner

print("=" * 60)
print("阶段24测试：单元测试框架")
print("=" * 60)

# 测试1：验证TestCase初始化
print("\n[测试1] 验证TestCase初始化")
try:
    tc = TestCase()
    print("✅ TestCase初始化成功")
    print(f"   passed: {tc.passed}")
    print(f"   failed: {tc.failed}")
except Exception as e:
    print(f"❌ TestCase初始化失败: {e}")

# 测试2：验证断言功能
print("\n[测试2] 验证断言功能")
try:
    tc = TestCase()
    
    # 测试assert_equal
    tc.assert_equal(1 + 1, 2)
    print("✅ assert_equal 通过")
    
    # 测试assert_true
    tc.assert_true(True)
    print("✅ assert_true 通过")
    
    # 测试assert_false
    tc.assert_false(False)
    print("✅ assert_false 通过")
    
    # 测试assert_in
    tc.assert_in(1, [1, 2, 3])
    print("✅ assert_in 通过")
    
    # 测试assert_not_none
    tc.assert_not_none("test")
    print("✅ assert_not_none 通过")
    
except AssertionError as e:
    print(f"❌ 断言失败: {e}")
except Exception as e:
    print(f"❌ 断言测试异常: {e}")

# 测试3：验证run_test方法
print("\n[测试3] 验证run_test方法")
try:
    tc = TestCase()
    
    def success_test():
        tc.assert_equal(1, 1)
    
    def fail_test():
        tc.assert_equal(1, 2)
    
    # 运行成功测试
    result1 = tc.run_test("success_test", success_test)
    print(f"   成功测试: {'通过' if result1 else '失败'}")
    
    # 运行失败测试
    result2 = tc.run_test("fail_test", fail_test)
    print(f"   失败测试: {'通过' if result2 else '失败'}")
    
    print(f"   统计: passed={tc.passed}, failed={tc.failed}")
    
    if tc.passed == 1 and tc.failed == 1:
        print("✅ run_test方法测试通过")
    else:
        print("❌ run_test方法统计不正确")
        
except Exception as e:
    print(f"❌ run_test方法测试失败: {e}")
    import traceback
    traceback.print_exc()

# 测试4：验证TestRunner
print("\n[测试4] 验证TestRunner")
try:
    class SampleTest(TestCase):
        def test_pass(self):
            self.assert_equal(1, 1)
        
        def test_fail(self):
            self.assert_equal(1, 2)
    
    runner = TestRunner()
    runner.add_test_case(SampleTest())
    result = runner.run_all()
    
    if runner.total_passed == 1 and runner.total_failed == 1:
        print("✅ TestRunner测试通过")
    else:
        print(f"❌ TestRunner统计不正确: passed={runner.total_passed}, failed={runner.total_failed}")
        
except Exception as e:
    print(f"❌ TestRunner测试失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("阶段24测试完成！")
print("=" * 60)
