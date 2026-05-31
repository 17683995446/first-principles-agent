"""阶段69：逻辑回归测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import LogisticRegression

def test_logistic_regression():
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

    lr = LogisticRegression(learning_rate=0.1, epochs=2000)
    lr.fit(X, y)

    # 测试分类预测
    assert lr.predict([1, 1]) == 0
    assert lr.predict([4, 4]) == 1

    # 测试概率输出
    prob0 = lr.predict_proba([1, 1])
    prob1 = lr.predict_proba([4, 4])
    assert prob0 < 0.5
    assert prob1 > 0.5

    # 测试批量预测
    preds = lr.predict_batch([[1, 1], [4, 4], [2, 2]])
    assert preds == [0, 1, 0]

    print("✅ 阶段69 逻辑回归测试通过")

if __name__ == "__main__":
    test_logistic_regression()
