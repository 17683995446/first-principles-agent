"""阶段61：模拟退火测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import SimulatedAnnealing

def test_simulated_annealing():
    sa = SimulatedAnnealing(initial_temp=100, cooling_rate=0.95)

    # 测试接受概率
    assert sa.acceptance_probability(10, 5, 100) == 1.0
    prob = sa.acceptance_probability(5, 10, 100)
    assert 0 < prob < 1

    # 测试优化
    def cost(sol):
        return sum((x - 3) ** 2 for x in sol)

    def neighbor(sol):
        new_sol = sol[:]
        idx = __import__('random').randint(0, len(new_sol) - 1)
        new_sol[idx] += __import__('random').uniform(-1, 1)
        return new_sol

    initial = [0.0, 0.0]
    best, best_cost = sa.optimize(initial, neighbor, cost, max_iterations=500)
    assert len(best) == 2
    assert best_cost < cost(initial)

    print("✅ 阶段61 模拟退火测试通过")

if __name__ == "__main__":
    test_simulated_annealing()
