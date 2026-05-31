"""阶段66：K均值聚类测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import KMeans

def test_kmeans():
    X = [
        [1, 1], [1, 2], [2, 1], [2, 2],
        [8, 8], [8, 9], [9, 8], [9, 9],
        [5, 5], [5, 6], [6, 5], [6, 6]
    ]

    kmeans = KMeans(k=3, max_iters=100)
    kmeans.fit(X)

    # 测试聚类中心
    assert len(kmeans.centroids) == 3
    assert len(kmeans.centroids[0]) == 2

    # 测试预测
    labels = kmeans.predict(X)
    assert len(labels) == len(X)
    assert all(0 <= l < 3 for l in labels)

    # 测试同一簇的点标签相同
    cluster_0 = [i for i, l in enumerate(labels) if l == labels[0]]
    assert len(cluster_0) >= 2

    print("✅ 阶段66 K均值聚类测试通过")

if __name__ == "__main__":
    test_kmeans()
