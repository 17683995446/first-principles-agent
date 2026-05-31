"""阶段70：决策森林测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import RandomForest

def test_random_forest():
    X = [
        [1, 1], [1, 2], [2, 1], [2, 2],
        [5, 5], [5, 6], [6, 5], [6, 6]
    ]
    y = [0, 0, 0, 0, 1, 1, 1, 1]

    rf = RandomForest(n_trees=5, max_depth=3)
    rf.fit(X, y)

    # 测试预测
    assert rf.predict([1, 1]) == 0
    assert rf.predict([6, 6]) == 1

    # 测试批量预测
    preds = rf.predict_batch([[1, 1], [6, 6], [2, 2]])
    assert preds[0] == 0
    assert preds[1] == 1
    assert preds[2] == 0

    # 测试特征重要性
    importances = rf.feature_importance(X, y)
    assert len(importances) == 2
    assert abs(sum(importances) - 1.0) < 0.01

    print("✅ 阶段70 决策森林测试通过")

if __name__ == "__main__":
    test_random_forest()
