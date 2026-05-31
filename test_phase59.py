"""阶段59：蚁群算法测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import AntColony

def test_ant_colony():
    n = 4
    ac = AntColony(n_nodes=n)

    # 设置距离矩阵
    dist = [
        [0, 1, 2, 3],
        [1, 0, 1, 2],
        [2, 1, 0, 1],
        [3, 2, 1, 0]
    ]
    ac.set_distances(dist)

    # 测试路径构建
    path = ac._construct_path()
    assert len(path) == n
    assert len(set(path)) == n

    # 测试路径长度
    length = ac._path_length([0, 1, 2, 3])
    assert length > 0

    # 测试求解
    best_path, best_length = ac.solve(iterations=20, n_ants=5)
    assert best_path is not None
    assert best_length > 0
    assert len(best_path) == n

    print("✅ 阶段59 蚁群算法测试通过")

if __name__ == "__main__":
    test_ant_colony()
