"""阶段88：中介者模式测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import MediatorPattern, Colleague

def test_mediator_pattern():
    mediator = MediatorPattern()
    c1 = Colleague("Alice")
    c2 = Colleague("Bob")
    c3 = Colleague("Charlie")

    mediator.register("Alice", c1)
    mediator.register("Bob", c2)
    mediator.register("Charlie", c3)

    # 测试点对点消息
    c1.send("Hello Bob", "Bob")
    assert len(c2.get_received()) == 1
    assert c2.get_received()[0]["message"] == "Hello Bob"
    assert c2.get_received()[0]["sender"] == "Alice"

    # 测试广播
    c1.send("Hello all")
    assert len(c2.get_received()) == 2
    assert len(c3.get_received()) == 1

    # 测试消息历史
    assert len(mediator.get_messages()) == 3

    print("✅ 阶段88 中介者模式测试通过")

if __name__ == "__main__":
    test_mediator_pattern()
