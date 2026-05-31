"""阶段64：隐马尔可夫模型测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import HMM

def test_hmm():
    states = ["Sunny", "Rainy"]
    observations = ["walk", "shop", "clean"]
    hmm = HMM(states, observations)

    # 测试参数设置
    hmm.set_initial({"Sunny": 0.6, "Rainy": 0.4})
    hmm.set_transition({
        "Sunny": {"Sunny": 0.7, "Rainy": 0.3},
        "Rainy": {"Sunny": 0.4, "Rainy": 0.6}
    })
    hmm.set_emission({
        "Sunny": {"walk": 0.6, "shop": 0.3, "clean": 0.1},
        "Rainy": {"walk": 0.1, "shop": 0.4, "clean": 0.5}
    })

    # 测试前向算法
    alpha = hmm.forward(["walk", "shop"])
    assert len(alpha) == 2
    assert all(s in alpha[0] for s in states)

    # 测试维特比算法
    path = hmm.viterbi(["walk", "shop", "clean"])
    assert len(path) == 3
    assert all(s in states for s in path)

    # 测试参数学习
    obs_list = [["walk", "shop"], ["shop", "clean"], ["walk", "clean"]]
    hmm.baum_welch(obs_list, iterations=5)
    assert sum(hmm.initial.values()) > 0

    print("✅ 阶段64 隐马尔可夫模型测试通过")

if __name__ == "__main__":
    test_hmm()
