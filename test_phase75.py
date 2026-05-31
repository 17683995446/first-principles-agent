"""阶段75：情感分析测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import SentimentAnalyzer

def test_sentiment_analyzer():
    sa = SentimentAnalyzer()

    # 测试正面情感
    result = sa.analyze("this is a great and amazing product")
    assert result["polarity"] == "positive"
    assert result["score"] > 0
    assert result["intensity"] > 0

    # 测试负面情感
    result = sa.analyze("this is a terrible and awful experience")
    assert result["polarity"] == "negative"
    assert result["score"] < 0

    # 测试中性情感
    result = sa.analyze("this is a book")
    assert result["polarity"] == "neutral"
    assert result["score"] == 0

    # 测试否定
    result = sa.analyze("not good")
    assert result["score"] < 0

    # 测试强度修饰
    result = sa.analyze("very good")
    assert result["score"] > 1

    # 测试批量分析
    results = sa.analyze_batch(["good", "bad", "okay"])
    assert len(results) == 3
    assert results[0]["polarity"] == "positive"
    assert results[1]["polarity"] == "negative"
    assert results[2]["polarity"] == "neutral"

    print("✅ 阶段75 情感分析测试通过")

if __name__ == "__main__":
    test_sentiment_analyzer()
