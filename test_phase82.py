"""阶段82：装饰器模式测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import DecoratorPattern, ConcreteDecoratorA, ConcreteDecoratorB

class Component:
    def operation(self):
        return "Component"

def test_decorator_pattern():
    comp = Component()

    # 测试基础组件
    assert comp.operation() == "Component"

    # 测试单层装饰
    dec_a = ConcreteDecoratorA(comp)
    assert dec_a.operation() == "DecoratorA(Component)"

    # 测试多层装饰
    dec_ab = ConcreteDecoratorB(ConcreteDecoratorA(comp))
    assert dec_ab.operation() == "DecoratorA(Component)[DecoratorB]"

    # 测试透明包装（属性透传）
    assert dec_a.operation == dec_a.operation

    print("✅ 阶段82 装饰器模式测试通过")

if __name__ == "__main__":
    test_decorator_pattern()
