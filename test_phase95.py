"""阶段95：外观模式测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import FacadePattern

class SubsystemA:
    def operation_a(self, x):
        return f"A:{x}"

class SubsystemB:
    def operation_b(self, x, y):
        return x + y

def test_facade_pattern():
    facade = FacadePattern()
    facade.register("A", SubsystemA())
    facade.register("B", SubsystemB())

    # 测试统一接口调用
    assert facade.call("A", "operation_a", "test") == "A:test"
    assert facade.call("B", "operation_b", 3, 4) == 7

    # 测试获取子系统
    assert set(facade.get_subsystems()) == {"A", "B"}

    # 测试未知子系统
    try:
        facade.call("C", "method")
        assert False, "应该抛出异常"
    except ValueError:
        pass

    print("✅ 阶段95 外观模式测试通过")

if __name__ == "__main__":
    test_facade_pattern()
