"""阶段76：命令模式测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import CommandPattern, AddCommand

class Receiver:
    def __init__(self):
        self.value = 0

def test_command_pattern():
    receiver = Receiver()
    cmd = CommandPattern()

    # 测试执行
    assert cmd.execute(AddCommand(receiver, 5)) == 5
    assert cmd.execute(AddCommand(receiver, 3)) == 8
    assert receiver.value == 8

    # 测试撤销
    assert cmd.undo() == 5
    assert receiver.value == 5

    # 测试重做
    assert cmd.redo() == 8
    assert receiver.value == 8

    # 测试命令队列
    cmd2 = CommandPattern()
    r2 = Receiver()
    cmd2.enqueue(AddCommand(r2, 1))
    cmd2.enqueue(AddCommand(r2, 2))
    cmd2.enqueue(AddCommand(r2, 3))
    results = cmd2.process_queue()
    assert results == [1, 3, 6]
    assert r2.value == 6

    # 测试历史记录
    assert len(cmd.get_history()) == 2
    cmd.clear_history()
    assert len(cmd.get_history()) == 0
    assert cmd.undo() is None
    assert cmd.redo() is None

    print("✅ 阶段76 命令模式测试通过")

if __name__ == "__main__":
    test_command_pattern()
