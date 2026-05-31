"""阶段68：线性回归测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import LinearRegression

def test_linear_regression():
    X = [1, 2, 3, 4, 5]
    y = [2, 4, 6, 8, 10]

    lr = LinearRegression()
    lr.fit(X, y)

    # 测试拟合系数
    assert abs(lr.coef - 2.0) < 0.01, f"系数错误: {lr.coef}"
    assert abs(lr.intercept - 0.0) < 0.01, f"截距错误: {lr.intercept}"

    # 测试预测
    preds = lr.predict([6, 7, 8])
    assert abs(preds[0] - 12) < 0.1
    assert abs(preds[1] - 14) < 0.1
    assert abs(preds[2] - 16) < 0.1

    # 测试R²分数
    score = lr.score(X, y)
    assert score > 0.99

    # 测试MSE
    mse = lr.mse(X, y)
    assert mse < 0.1

    print("✅ 阶段68 线性回归测试通过")

if __name__ == "__main__":
    test_linear_regression()
