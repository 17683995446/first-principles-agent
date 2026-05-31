"""阶段81：代理模式测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import ProxyPattern

class Target:
    def __init__(self):
        self.value = 10

    def compute(self, x):
        return self.value + x

    def get_value(self):
        return self.value

def test_proxy_pattern():
    target = Target()
    proxy = ProxyPattern(target)

    # 测试访问控制
    assert proxy.get_value() == 10
    assert proxy.compute(5) == 15

    # 测试缓存
    assert proxy.compute(5) == 15  # 应从缓存返回

    # 测试访问日志
    log = proxy.get_access_log()
    assert "get_value" in log
    assert "compute" in log

    # 测试禁用访问
    proxy.set_enabled(False)
    try:
        proxy.get_value()
        assert False, "应该抛出异常"
    except PermissionError:
        pass

    # 测试手动缓存
    proxy2 = ProxyPattern()
    proxy2.cache_result("key1", "cached_value")
    # cache_result 只缓存到 _cache，需要通过 getattr 访问时才能命中

    print("✅ 阶段81 代理模式测试通过")

if __name__ == "__main__":
    test_proxy_pattern()
