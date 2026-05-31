"""阶段89：备忘录模式测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import MementoPattern

def test_memento_pattern():
    memento = MementoPattern()

    # 测试状态保存
    idx1 = memento.save({"state": 1})
    idx2 = memento.save({"state": 2})
    idx3 = memento.save({"state": 3})

    assert idx1 == 0
    assert idx2 == 1
    assert idx3 == 2

    # 测试撤销
    assert memento.undo()["state"] == 2
    assert memento.undo()["state"] == 1
    assert memento.undo() is None  # 不能再撤销

    # 测试重做
    assert memento.redo()["state"] == 2
    assert memento.redo()["state"] == 3
    assert memento.redo() is None  # 不能再重做

    # 测试恢复到指定索引
    assert memento.restore(0)["state"] == 1

    # 测试历史记录
    assert len(memento.get_history()) == 3

    print("✅ 阶段89 备忘录模式测试通过")

if __name__ == "__main__":
    test_memento_pattern()
