"""阶段79：工厂模式测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import FactoryPattern

def test_factory_pattern():
    factory = FactoryPattern()

    factory.register("dict", lambda: {})
    factory.register("list", lambda: [])
    factory.register("int", lambda v: v)

    # 测试对象创建
    d = factory.create("dict")
    assert isinstance(d, dict)
    l = factory.create("list")
    assert isinstance(l, list)

    # 测试延迟初始化
    s1 = factory.get_or_create("singleton_dict", lambda: {"created": True})
    s2 = factory.get_or_create("singleton_dict", lambda: {"created": True})
    assert s1 is s2

    # 测试获取注册类型
    assert set(factory.get_registered()) == {"dict", "list", "int", "singleton_dict"}

    # 测试未知类型
    try:
        factory.create("unknown")
        assert False, "应该抛出异常"
    except ValueError:
        pass

    print("✅ 阶段79 工厂模式测试通过")

if __name__ == "__main__":
    test_factory_pattern()
