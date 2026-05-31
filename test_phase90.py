"""阶段90：访问者模式测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import VisitorPattern

class ElementA:
    def __init__(self, value):
        self.value = value

class ElementB:
    def __init__(self, value):
        self.value = value

def test_visitor_pattern():
    visitor = VisitorPattern()

    visitor.register(ElementA, lambda e: f"A:{e.value}")
    visitor.register(ElementB, lambda e: f"B:{e.value}")

    a = ElementA(10)
    b = ElementB(20)

    # 测试双重分发
    assert visitor.visit(a) == "A:10"
    assert visitor.visit(b) == "B:20"

    # 测试未注册类型
    class Unknown:
        pass
    assert visitor.visit(Unknown()) is None

    print("✅ 阶段90 访问者模式测试通过")

if __name__ == "__main__":
    test_visitor_pattern()
