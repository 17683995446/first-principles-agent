"""阶段84：桥接模式测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import BridgePattern, BridgeImplementationA, BridgeImplementationB

def test_bridge_pattern():
    impl_a = BridgeImplementationA()
    impl_b = BridgeImplementationB()

    bridge = BridgePattern(impl_a)
    assert bridge.operation() == "ImplementationA"

    # 测试动态切换实现
    bridge.set_implementation(impl_b)
    assert bridge.operation() == "ImplementationB"

    print("✅ 阶段84 桥接模式测试通过")

if __name__ == "__main__":
    test_bridge_pattern()
