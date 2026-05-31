"""阶段55：决策树测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import DecisionTree

def test_decision_tree():
    X = [
        [1, 1],
        [1, 2],
        [2, 1],
        [2, 2],
        [3, 3],
        [3, 4],
        [4, 3],
        [4, 4]
    ]
    y = [0, 0, 0, 0, 1, 1, 1, 1]

    tree = DecisionTree(max_depth=3)
    tree.fit(X, y)

    # 测试预测
    assert tree.predict([1, 1]) == 0
    assert tree.predict([4, 4]) == 1

    # 测试批量预测
    preds = tree.predict_batch([[1, 1], [4, 4], [2, 2]])
    assert preds[0] == 0
    assert preds[1] == 1
    assert preds[2] == 0

    print("✅ 阶段55 决策树测试通过")

if __name__ == "__main__":
    test_decision_tree()
