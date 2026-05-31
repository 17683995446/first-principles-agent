"""阶段96：抽象工厂测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import AbstractFactory, FactoryPattern

def test_abstract_factory():
    af = AbstractFactory()

    # 创建两个产品族的工厂
    factory_a = FactoryPattern()
    factory_a.register("product1", lambda: "A-Product1")
    factory_a.register("product2", lambda: "A-Product2")

    factory_b = FactoryPattern()
    factory_b.register("product1", lambda: "B-Product1")
    factory_b.register("product2", lambda: "B-Product2")

    af.register("FamilyA", factory_a)
    af.register("FamilyB", factory_b)

    # 测试产品族创建
    assert af.create("FamilyA", "product1") == "A-Product1"
    assert af.create("FamilyA", "product2") == "A-Product2"
    assert af.create("FamilyB", "product1") == "B-Product1"
    assert af.create("FamilyB", "product2") == "B-Product2"

    # 测试获取产品族
    assert set(af.get_families()) == {"FamilyA", "FamilyB"}

    # 测试未知产品族
    try:
        af.create("FamilyC", "product1")
        assert False, "应该抛出异常"
    except ValueError:
        pass

    print("✅ 阶段96 抽象工厂测试通过")

if __name__ == "__main__":
    test_abstract_factory()
