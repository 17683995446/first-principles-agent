"""阶段62：蒙特卡洛方法测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import MonteCarlo

def test_monte_carlo():
    mc = MonteCarlo(seed=42)

    # 测试随机采样
    samples = mc.sample("uniform", 100)
    assert len(samples) == 100
    assert all(0 <= s <= 1 for s in samples)

    normal_samples = mc.sample("normal", 100)
    assert len(normal_samples) == 100

    # 测试概率估计
    prob = mc.estimate_probability(lambda: __import__('random').random() > 0.5, n_samples=1000)
    assert 0.4 < prob < 0.6

    # 测试数值积分
    result = mc.integrate(lambda x: x ** 2, 0, 1, n_samples=10000)
    assert abs(result - 1/3) < 0.05

    # 测试PI估计
    pi_est = mc.estimate_pi(n_samples=50000)
    assert abs(pi_est - 3.14159) < 0.1

    print("✅ 阶段62 蒙特卡洛方法测试通过")

if __name__ == "__main__":
    test_monte_carlo()
