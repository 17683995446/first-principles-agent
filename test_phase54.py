"""阶段54：状态机测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import StateMachine

def test_state_machine():
    sm = StateMachine("idle")
    sm.add_state("idle")
    sm.add_state("running")
    sm.add_state("stopped")

    # 测试转换规则
    sm.add_transition("idle", "start", "running")
    sm.add_transition("running", "stop", "stopped")
    sm.add_transition("stopped", "reset", "idle")

    assert sm.current_state == "idle"

    # 测试事件触发
    assert sm.trigger("start") == True
    assert sm.current_state == "running"

    assert sm.trigger("stop") == True
    assert sm.current_state == "stopped"

    # 测试无效事件
    assert sm.trigger("start") == False

    # 测试可用事件
    assert sm.get_available_events() == ["reset"]

    # 测试历史
    assert len(sm.history) == 2

    print("✅ 阶段54 状态机测试通过")

if __name__ == "__main__":
    test_state_machine()
