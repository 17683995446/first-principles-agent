"""阶段60：粒子群优化测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import ParticleSwarm

def test_particle_swarm():
    pso = ParticleSwarm(n_particles=20, dim=2, bounds=[(-5, 5), (-5, 5)])

    # 测试初始化
    pso.initialize()
    assert len(pso.particles) == 20
    assert len(pso.particles[0]) == 2

    # 测试适应度
    fit = pso.fitness([0, 0])
    assert fit == 0

    # 测试优化
    best, best_fit = pso.optimize(iterations=50)
    assert len(best) == 2
    assert best_fit >= 0
    # 最优解应在0附近
    assert abs(best[0]) < 1.0, f"x1未收敛: {best[0]}"
    assert abs(best[1]) < 1.0, f"x2未收敛: {best[1]}"

    print("✅ 阶段60 粒子群优化测试通过")

if __name__ == "__main__":
    test_particle_swarm()
