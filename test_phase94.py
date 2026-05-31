"""阶段94：原型模式测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import PrototypePattern

def test_prototype_pattern():
    proto = PrototypePattern()

    original = {"name": "original", "items": [1, 2, 3]}
    proto.register("dict_proto", original)

    # 测试深拷贝
    clone1 = proto.clone("dict_proto", deep=True)
    assert clone1 == original
    clone1["items"].append(4)
    assert len(original["items"]) == 3  # 原对象不受影响

    # 测试浅拷贝
    clone2 = proto.clone("dict_proto", deep=False)
    clone2["items"].append(4)
    # 浅拷贝共享嵌套对象

    # 测试覆盖属性
    clone3 = proto.clone("dict_proto", deep=True, overrides={"name": "overridden"})
    assert clone3["name"] == "overridden"

    # 测试获取注册列表
    assert proto.get_registered() == ["dict_proto"]

    print("✅ 阶段94 原型模式测试通过")

if __name__ == "__main__":
    test_prototype_pattern()
