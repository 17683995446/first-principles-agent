"""阶段80：单例模式测试"""
import sys
import threading
sys.path.insert(0, '/workspace')
from first_principles_agent import SingletonPattern

def test_singleton_pattern():
    SingletonPattern.reset()

    s1 = SingletonPattern()
    s2 = SingletonPattern()
    assert s1 is s2

    s3 = SingletonPattern.get_instance()
    assert s1 is s3

    # 测试线程安全
    SingletonPattern.reset()
    instances = []
    lock = threading.Lock()

    def create_instance():
        inst = SingletonPattern()
        with lock:
            instances.append(inst)

    threads = [threading.Thread(target=create_instance) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(set(id(i) for i in instances)) == 1

    print("✅ 阶段80 单例模式测试通过")

if __name__ == "__main__":
    test_singleton_pattern()
