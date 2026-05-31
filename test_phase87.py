"""阶段87：责任链模式测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import ChainOfResponsibility

def test_chain_of_responsibility():
    chain = ChainOfResponsibility()

    def handler1(request):
        if request < 10:
            return f"handled_by_1:{request}"
        return None

    def handler2(request):
        if request < 20:
            return f"handled_by_2:{request}"
        return None

    def handler3(request):
        return f"handled_by_3:{request}"

    chain.add_handler(handler1).add_handler(handler2).add_handler(handler3)

    # 测试请求传递
    assert chain.handle(5) == "handled_by_1:5"
    assert chain.handle(15) == "handled_by_2:15"
    assert chain.handle(25) == "handled_by_3:25"

    # 测试动态链
    chain2 = ChainOfResponsibility()
    chain2.set_handlers([handler2])
    assert chain2.handle(5) == "handled_by_2:5"
    assert chain2.handle(25) is None

    print("✅ 阶段87 责任链模式测试通过")

if __name__ == "__main__":
    test_chain_of_responsibility()
