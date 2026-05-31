"""阶段91：迭代器模式测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import IteratorPattern, ReverseIteratorPattern

def test_iterator_pattern():
    data = [1, 2, 3, 4, 5]

    # 测试正向迭代器
    it = IteratorPattern(data)
    result = list(it)
    assert result == [1, 2, 3, 4, 5]

    # 测试has_next和reset
    it2 = IteratorPattern(data)
    assert it2.has_next()
    assert next(it2) == 1
    it2.reset()
    assert next(it2) == 1

    # 测试反向迭代器
    rit = ReverseIteratorPattern(data)
    result = list(rit)
    assert result == [5, 4, 3, 2, 1]

    # 测试反向has_next
    rit2 = ReverseIteratorPattern(data)
    assert rit2.has_next()
    assert next(rit2) == 5

    print("✅ 阶段91 迭代器模式测试通过")

if __name__ == "__main__":
    test_iterator_pattern()
