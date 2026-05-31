#!/usr/bin/env python3
"""
阶段24：单元测试框架
提供简单的测试运行器和断言功能
"""
import sys
import os
import traceback
from datetime import datetime

class TestCase:
    """测试用例基类"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def assert_equal(self, actual, expected, message=""):
        """断言相等"""
        if actual != expected:
            raise AssertionError(f"{message}\n  期望值: {expected}\n  实际值: {actual}")
    
    def assert_true(self, condition, message=""):
        """断言为真"""
        if not condition:
            raise AssertionError(f"{message}\n  条件不为真")
    
    def assert_false(self, condition, message=""):
        """断言为假"""
        if condition:
            raise AssertionError(f"{message}\n  条件不为假")
    
    def assert_in(self, item, container, message=""):
        """断言包含"""
        if item not in container:
            raise AssertionError(f"{message}\n  {item} 不在 {container} 中")
    
    def assert_not_none(self, obj, message=""):
        """断言不为None"""
        if obj is None:
            raise AssertionError(f"{message}\n  对象为None")
    
    def run_test(self, test_name, test_func):
        """运行单个测试"""
        try:
            test_func()
            self.passed += 1
            print(f"  ✅ {test_name}")
            return True
        except AssertionError as e:
            self.failed += 1
            error_msg = f"❌ {test_name}\n    {str(e)}"
            self.errors.append(error_msg)
            print(error_msg)
            return False
        except Exception as e:
            self.failed += 1
            error_msg = f"❌ {test_name}\n    异常: {type(e).__name__}: {str(e)}"
            self.errors.append(error_msg)
            print(error_msg)
            return False


class TestRunner:
    """测试运行器"""
    
    def __init__(self):
        self.test_cases = []
        self.total_passed = 0
        self.total_failed = 0
    
    def add_test_case(self, test_case):
        """添加测试用例"""
        self.test_cases.append(test_case)
    
    def run_all(self):
        """运行所有测试"""
        print("=" * 60)
        print("单元测试框架")
        print("=" * 60)
        
        start_time = datetime.now()
        
        for test_case in self.test_cases:
            print(f"\n运行测试: {test_case.__class__.__name__}")
            # 自动运行所有以test_开头的方法
            for method_name in dir(test_case):
                if method_name.startswith("test_"):
                    method = getattr(test_case, method_name)
                    if callable(method):
                        test_case.run_test(method_name, method)
            
            self.total_passed += test_case.passed
            self.total_failed += test_case.failed
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # 打印总结
        print("\n" + "=" * 60)
        print("测试总结")
        print("=" * 60)
        print(f"总测试数: {self.total_passed + self.total_failed}")
        print(f"通过: {self.total_passed} ✅")
        print(f"失败: {self.total_failed} ❌")
        print(f"耗时: {duration:.2f}秒")
        
        if self.total_failed == 0:
            print("\n🎉 所有测试通过！")
        else:
            print(f"\n⚠️  {self.total_failed} 个测试失败")
        
        return self.total_failed == 0


# 示例测试用例
class ExampleTest(TestCase):
    """示例测试"""
    
    def test_assertions(self):
        """测试断言功能"""
        self.assert_equal(1 + 1, 2, "1+1应该等于2")
        self.assert_true(True, "True应该为真")
        self.assert_false(False, "False应该为假")
        self.assert_in(1, [1, 2, 3], "1应该在列表中")
        self.assert_not_none("not none", "字符串不应为None")


if __name__ == "__main__":
    # 运行示例测试
    runner = TestRunner()
    runner.add_test_case(ExampleTest())
    runner.run_all()
