"""阶段65：支持向量机测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import SVM

def test_svm():
    X = [
        [2, 3],
        [1, 2],
        [2, 1],
        [3, 2],
        [5, 6],
        [6, 5],
        [5, 4],
        [6, 7]
    ]
    y = [1, 1, 1, 1, -1, -1, -1, -1]

    svm = SVM(learning_rate=0.01, lambda_param=0.01, epochs=1000)
    svm.fit(X, y)

    # 测试分类
    assert svm.predict([1, 1]) == 1
    assert svm.predict([6, 6]) == -1

    # 测试批量预测
    preds = svm.predict_batch([[1, 1], [6, 6], [2, 2]])
    assert preds[0] == 1
    assert preds[1] == -1
    assert preds[2] == 1

    # 测试决策函数
    df = svm.decision_function([1, 1])
    assert isinstance(df, float)

    print("✅ 阶段65 支持向量机测试通过")

if __name__ == "__main__":
    test_svm()
