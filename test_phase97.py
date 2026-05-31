"""阶段97：依赖注入测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import DependencyInjection

class ServiceA:
    def __init__(self):
        self.name = "ServiceA"

class ServiceB:
    def __init__(self):
        self.name = "ServiceB"

def test_dependency_injection():
    di = DependencyInjection()

    # 测试注册和解析
    di.register("ServiceA", ServiceA, singleton=False)
    di.register("ServiceB", ServiceB, singleton=True)

    s1 = di.resolve("ServiceA")
    s2 = di.resolve("ServiceA")
    assert s1.name == "ServiceA"
    assert s1 is not s2  # 非单例

    s3 = di.resolve("ServiceB")
    s4 = di.resolve("ServiceB")
    assert s3 is s4  # 单例

    # 测试获取注册列表
    assert set(di.get_registrations()) == {"ServiceA", "ServiceB"}

    # 测试未注册解析
    try:
        di.resolve("Unknown")
        assert False, "应该抛出异常"
    except ValueError:
        pass

    print("✅ 阶段97 依赖注入测试通过")

if __name__ == "__main__":
    test_dependency_injection()
