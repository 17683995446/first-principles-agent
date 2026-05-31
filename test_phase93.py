"""阶段93：构建器模式测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import BuilderPattern

def test_builder_pattern():
    builder = BuilderPattern()

    # 测试分步构建
    product = builder.set("name", "Product1").set("price", 100).set("category", "A").build()
    assert product["name"] == "Product1"
    assert product["price"] == 100
    assert product["category"] == "A"

    # 测试reset
    builder.reset().set("key", "value")
    product2 = builder.build()
    assert product2 == {"key": "value"}

    # 测试build返回副本
    p1 = builder.set("a", 1).build()
    p2 = builder.build()
    p1["a"] = 2
    assert p2["a"] == 1  # p2不应受影响

    print("✅ 阶段93 构建器模式测试通过")

if __name__ == "__main__":
    test_builder_pattern()
