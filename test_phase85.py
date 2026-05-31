"""阶段85：组合模式测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import CompositePattern

def test_composite_pattern():
    root = CompositePattern("root")
    child1 = CompositePattern("child1")
    child2 = CompositePattern("child2")
    grandchild = CompositePattern("grandchild")

    root.add(child1).add(child2)
    child1.add(grandchild)

    # 测试树形结构
    assert root.operation() == ["root", "child1", "grandchild", "child2"]

    # 测试获取子节点
    assert len(root.get_children()) == 2
    assert len(child1.get_children()) == 1

    # 测试移除
    child1.remove(grandchild)
    assert len(child1.get_children()) == 0

    print("✅ 阶段85 组合模式测试通过")

if __name__ == "__main__":
    test_composite_pattern()
