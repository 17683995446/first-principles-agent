"""阶段86：享元模式测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import FlyweightPattern

def test_flyweight_pattern():
    FlyweightPattern.clear_pool()

    f1 = FlyweightPattern("key1", color="red")
    f2 = FlyweightPattern("key1", color="red")
    f3 = FlyweightPattern("key2", color="blue")

    # 测试对象共享
    assert f1 is f2
    assert f1 is not f3

    # 测试状态分离
    assert f1.get_key() == "key1"
    assert f1.get_state()["color"] == "red"
    assert f3.get_state()["color"] == "blue"

    # 测试内存优化（池大小）
    assert FlyweightPattern.get_pool_size() == 2

    FlyweightPattern.clear_pool()
    assert FlyweightPattern.get_pool_size() == 0

    print("✅ 阶段86 享元模式测试通过")

if __name__ == "__main__":
    test_flyweight_pattern()
