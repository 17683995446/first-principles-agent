"""阶段67：主成分分析测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import PCA

def test_pca():
    X = [
        [1, 2, 3],
        [4, 5, 7],
        [7, 8, 10],
        [10, 11, 14]
    ]

    pca = PCA(n_components=2)

    # 测试fit
    pca.fit(X)
    assert len(pca.components) == 2
    assert len(pca.components[0]) == 3

    # 测试transform
    transformed = pca.transform(X)
    assert len(transformed) == len(X)
    assert len(transformed[0]) == 2

    # 测试fit_transform
    pca2 = PCA(n_components=2)
    transformed2 = pca2.fit_transform(X)
    assert len(transformed2) == len(X)
    assert len(transformed2[0]) == 2

    # 测试方差保留（数据高度共线，应保留大部分方差）
    ratios = pca.explained_variance_ratio(X)
    assert len(ratios) == 2
    assert sum(ratios) > 0.8

    print("✅ 阶段67 主成分分析测试通过")

if __name__ == "__main__":
    test_pca()
