"""阶段100：服务总线测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import ServiceBus

def test_service_bus():
    bus = ServiceBus()

    # 测试服务注册和调用
    def echo_service(message):
        return f"echo:{message}"

    bus.register_service("echo", echo_service)
    assert bus.send("echo", "hello") == "echo:hello"

    # 测试事件订阅和发布
    events = []
    def handler1(msg):
        events.append(f"h1:{msg}")
        return "r1"

    def handler2(msg):
        events.append(f"h2:{msg}")
        return "r2"

    bus.subscribe("test_event", handler1)
    bus.subscribe("test_event", handler2)

    results = bus.publish("test_event", "data")
    assert len(results) == 2
    assert "r1" in results
    assert "r2" in results
    assert "h1:data" in events
    assert "h2:data" in events

    # 测试消息历史
    assert len(bus.get_history()) == 1

    # 测试获取服务列表
    assert bus.get_services() == ["echo"]

    # 测试未知服务
    try:
        bus.send("unknown", "msg")
        assert False, "应该抛出异常"
    except ValueError:
        pass

    print("✅ 阶段100 服务总线测试通过")

if __name__ == "__main__":
    test_service_bus()
