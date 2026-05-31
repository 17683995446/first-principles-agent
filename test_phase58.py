"""阶段58：遗传算法测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import GeneticAlgorithm

def test_genetic_algorithm():
    ga = GeneticAlgorithm(population_size=30, gene_length=10, mutation_rate=0.05)

    # 测试种群初始化
    ga.initialize()
    assert len(ga.population) == 30
    assert len(ga.population[0]) == 10

    # 测试适应度
    ind = [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
    assert ga.fitness(ind) == 5

    # 测试选择
    selected = ga.select()
    assert len(selected) == 10

    # 测试交叉
    p1 = [0] * 10
    p2 = [1] * 10
    c1, c2 = ga.crossover(p1, p2)
    assert len(c1) == 10
    assert len(c2) == 10

    # 测试变异
    original = [0] * 10
    mutated = ga.mutate(original)
    assert len(mutated) == 10

    # 测试进化
    best, best_fit = ga.evolve(generations=50)
    assert len(best) == 10
    assert best_fit >= 0

    print("✅ 阶段58 遗传算法测试通过")

if __name__ == "__main__":
    test_genetic_algorithm()
