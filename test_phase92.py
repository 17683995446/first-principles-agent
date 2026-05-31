"""阶段92：解释器模式测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import InterpreterPattern

def test_interpreter_pattern():
    interp = InterpreterPattern()

    # 测试基本运算
    assert interp.evaluate("+ 3 4") == 7
    assert interp.evaluate("- 10 3") == 7
    assert interp.evaluate("* 3 4") == 12
    assert interp.evaluate("/ 10 3") == 3

    # 测试变量
    interp.set_variable("x", 5)
    interp.set_variable("y", 3)
    assert interp.evaluate("+ x y") == 8

    # 测试嵌套表达式
    assert interp.evaluate("+ * 2 3 4") == 10  # (2*3) + 4

    print("✅ 阶段92 解释器模式测试通过")

if __name__ == "__main__":
    test_interpreter_pattern()
