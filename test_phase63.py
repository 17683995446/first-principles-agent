"""阶段63：马尔可夫链测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import MarkovChain

def test_markov_chain():
    states = ["A", "B", "C"]
    mc = MarkovChain(states)

    # 测试状态转移设置
    mc.set_transition("A", "A", 0.5)
    mc.set_transition("A", "B", 0.3)
    mc.set_transition("A", "C", 0.2)
    mc.set_transition("B", "A", 0.2)
    mc.set_transition("B", "B", 0.6)
    mc.set_transition("B", "C", 0.2)
    mc.set_transition("C", "A", 0.1)
    mc.set_transition("C", "B", 0.3)
    mc.set_transition("C", "C", 0.6)

    # 测试归一化
    mc.normalize()
    assert abs(sum(mc.transitions["A"].values()) - 1.0) < 0.01

    # 测试序列生成
    seq = mc.generate_sequence(10, "A")
    assert len(seq) == 10
    assert all(s in states for s in seq)

    # 测试稳态分布
    steady = mc.steady_state(iterations=500)
    assert abs(sum(steady.values()) - 1.0) < 0.01
    assert all(s in steady for s in states)

    print("✅ 阶段63 马尔可夫链测试通过")

if __name__ == "__main__":
    test_markov_chain()
