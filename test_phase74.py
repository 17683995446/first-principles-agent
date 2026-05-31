"""阶段74：文本分类测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import TextClassifier

def test_text_classifier():
    documents = [
        "the cat sat on the mat",
        "the dog sat on the log",
        "the cat chased the mouse",
        "the dog chased the cat",
        "a beautiful sunny day",
        "the weather is nice today",
        "it is raining outside",
        "cloudy sky today"
    ]
    labels = ["animal", "animal", "animal", "animal", "weather", "weather", "weather", "weather"]

    clf = TextClassifier()
    clf.fit(documents, labels)

    # 测试预测
    pred1 = clf.predict("the cat is sleeping")
    pred2 = clf.predict("it is snowing today")
    assert pred1 == "animal"
    assert pred2 == "weather"

    # 测试批量预测
    preds = clf.predict_batch(["the dog barked", "sunny and warm"])
    assert preds[0] == "animal"
    assert preds[1] == "weather"

    # 测试准确率
    score = clf.score(documents, labels)
    assert score > 0.5

    print("✅ 阶段74 文本分类测试通过")

if __name__ == "__main__":
    test_text_classifier()
