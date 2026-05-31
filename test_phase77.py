"""阶段77：观察者模式测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import ObserverPattern

def test_observer_pattern():
    obs = ObserverPattern()
    results = []

    def callback1(data):
        results.append(f"cb1:{data}")

    def callback2(data):
        results.append(f"cb2:{data}")

    # 测试订阅和通知
    obs.subscribe("event1", callback1)
    obs.subscribe("event1", callback2)
    obs.notify("event1", "hello")
    assert "cb1:hello" in results
    assert "cb2:hello" in results

    # 测试取消订阅
    results.clear()
    obs.unsubscribe("event1", callback1)
    obs.notify("event1", "world")
    assert "cb1:world" not in results
    assert "cb2:world" in results

    # 测试无订阅者事件
    assert obs.notify("unknown", "data") == []

    # 测试获取订阅者
    assert len(obs.get_subscribers("event1")) == 1
    assert len(obs.get_subscribers("unknown")) == 0

    print("✅ 阶段77 观察者模式测试通过")

if __name__ == "__main__":
    test_observer_pattern()
