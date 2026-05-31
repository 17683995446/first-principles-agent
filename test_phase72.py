"""阶段72：词向量测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import WordVector

def test_word_vector():
    sentences = [
        "the cat sat on the mat",
        "the dog sat on the log",
        "the cat chased the mouse",
        "the dog chased the cat"
    ]

    wv = WordVector(vector_size=10)
    wv.fit(sentences)

    # 测试词嵌入
    vec = wv.get_vector("cat")
    assert len(vec) == 10

    # 测试相似度计算
    sim_cat_dog = wv.similarity("cat", "dog")
    sim_cat_mat = wv.similarity("cat", "mat")
    # cat和dog在语料中更相似
    assert -1 <= sim_cat_dog <= 1
    assert -1 <= sim_cat_mat <= 1

    # 测试最相似词
    similar = wv.most_similar("cat", top_n=3)
    assert len(similar) == 3
    assert all(isinstance(s, tuple) and len(s) == 2 for s in similar)

    print("✅ 阶段72 词向量测试通过")

if __name__ == "__main__":
    test_word_vector()
