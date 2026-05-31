"""阶段83：适配器模式测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import AdapterPattern

class OldSystem:
    def old_method(self):
        return "old"

    def another_old(self):
        return "another"

def test_adapter_pattern():
    old = OldSystem()
    adapter = AdapterPattern(old, {"new_method": "old_method", "new_another": "another_old"})

    # 测试接口转换
    assert adapter.new_method() == "old"
    assert adapter.new_another() == "another"

    # 测试直接透传
    assert adapter.old_method() == "old"

    # 测试动态添加映射
    adapter.add_mapping("third", "another_old")
    assert adapter.third() == "another"

    print("✅ 阶段83 适配器模式测试通过")

if __name__ == "__main__":
    test_adapter_pattern()
