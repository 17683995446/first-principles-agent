"""阶段71：梯度提升测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import GradientBoosting

def test_gradient_boosting():
    X = [
        [1], [2], [3], [4], [5]
    ]
    y = [2, 4, 6, 8, 10]

    gb = GradientBoosting(n_estimators=20, learning_rate=0.2, max_depth=3)
    gb.fit(X, y)

    # 测试预测
    pred1 = gb.predict([1])
    pred2 = gb.predict([5])
    assert abs(pred1 - 2) < 3
    assert abs(pred2 - 10) < 3

    # 测试批量预测
    preds = gb.predict_batch([[1], [3], [5]])
    assert len(preds) == 3

    # 测试残差学习（预测应接近真实值）
    train_preds = gb.predict_batch(X)
    mse = sum((y[i] - train_preds[i]) ** 2 for i in range(len(y))) / len(y)
    assert mse < 10

    print("✅ 阶段71 梯度提升测试通过")

if __name__ == "__main__":
    test_gradient_boosting()
