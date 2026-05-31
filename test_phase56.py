"""阶段56：贝叶斯网络测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import BayesianNetwork

def test_bayesian_network():
    bn = BayesianNetwork()
    bn.add_node("Rain", ["yes", "no"])
    bn.add_node("Sprinkler", ["on", "off"])
    bn.add_node("Grass", ["wet", "dry"])

    bn.add_edge("Rain", "Sprinkler")
    bn.add_edge("Rain", "Grass")
    bn.add_edge("Sprinkler", "Grass")

    # 测试概率计算
    bn.set_cpt("Rain", {(): {"yes": 0.2, "no": 0.8}})

    # 测试推理
    result = bn.infer("Rain")
    assert "yes" in result
    assert "no" in result

    # 测试学习更新
    data = [
        {"Rain": "yes", "Sprinkler": "off", "Grass": "wet"},
        {"Rain": "no", "Sprinkler": "on", "Grass": "wet"},
        {"Rain": "no", "Sprinkler": "off", "Grass": "dry"},
    ]
    bn.update_cpt("Grass", data)
    assert "Grass" in bn.cpts

    print("✅ 阶段56 贝叶斯网络测试通过")

if __name__ == "__main__":
    test_bayesian_network()
