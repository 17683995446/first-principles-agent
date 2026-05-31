"""阶段73：TF-IDF测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import TFIDF

def test_tfidf():
    documents = [
        "the cat sat on the mat",
        "the dog sat on the log",
        "the cat chased the mouse",
        "the dog chased the cat"
    ]

    tfidf = TFIDF()

    # 测试fit
    tfidf.fit(documents)
    assert len(tfidf.vocab) > 0
    assert "cat" in tfidf.vocab
    assert "dog" in tfidf.vocab

    # 测试transform
    vectors = tfidf.transform(documents)
    assert len(vectors) == len(documents)
    assert len(vectors[0]) == len(tfidf.vocab)

    # 测试fit_transform
    tfidf2 = TFIDF()
    vectors2 = tfidf2.fit_transform(documents)
    assert len(vectors2) == len(documents)

    # 测试特征名
    features = tfidf.get_feature_names()
    assert len(features) == len(tfidf.vocab)

    # 测试权重：cat在文档中出现较多，idf应较低
    cat_idx = tfidf.vocab.index("cat")
    mouse_idx = tfidf.vocab.index("mouse")
    assert tfidf.idf["mouse"] >= tfidf.idf["cat"]

    print("✅ 阶段73 TF-IDF测试通过")

if __name__ == "__main__":
    test_tfidf()
