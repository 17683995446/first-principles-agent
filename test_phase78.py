"""阶段78：策略模式测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import StrategyPattern

def test_strategy_pattern():
    ctx = StrategyPattern()

    ctx.register("add", lambda a, b: a + b)
    ctx.register("sub", lambda a, b: a - b)
    ctx.register("mul", lambda a, b: a * b)

    # 测试动态切换
    ctx.set_strategy("add")
    assert ctx.execute(3, 4) == 7

    ctx.set_strategy("sub")
    assert ctx.execute(10, 3) == 7

    ctx.set_strategy("mul")
    assert ctx.execute(3, 4) == 12

    # 测试获取可用策略
    assert set(ctx.get_available()) == {"add", "sub", "mul"}

    # 测试未设置策略
    ctx2 = StrategyPattern()
    try:
        ctx2.execute(1, 2)
        assert False, "应该抛出异常"
    except ValueError:
        pass

    # 测试设置不存在的策略
    assert ctx.set_strategy("div") == False

    print("✅ 阶段78 策略模式测试通过")

if __name__ == "__main__":
    test_strategy_pattern()
