"""阶段57：神经网络测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import NeuralNetwork

def test_neural_network():
    # XOR问题 - 使用更大网络和更多轮数确保收敛
    X = [[0, 0], [0, 1], [1, 0], [1, 1]]
    y = [[0], [1], [1], [0]]

    # 多次尝试以确保收敛
    pred0 = pred1 = pred2 = pred3 = 0.5
    for attempt in range(5):
        nn = NeuralNetwork(layers=[2, 8, 1], learning_rate=0.5)
        nn.train(X, y, epochs=10000)

        pred0 = nn.predict([0, 0])[0]
        pred1 = nn.predict([0, 1])[0]
        pred2 = nn.predict([1, 0])[0]
        pred3 = nn.predict([1, 1])[0]

        if pred0 < 0.5 and pred1 > 0.5 and pred2 > 0.5 and pred3 < 0.5:
            break

    assert pred0 < 0.5, f"XOR(0,0)预测失败: {pred0}"
    assert pred1 > 0.5, f"XOR(0,1)预测失败: {pred1}"
    assert pred2 > 0.5, f"XOR(1,0)预测失败: {pred2}"
    assert pred3 < 0.5, f"XOR(1,1)预测失败: {pred3}"

    print("✅ 阶段57 神经网络测试通过")

if __name__ == "__main__":
    test_neural_network()
