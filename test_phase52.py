"""阶段52：工作流引擎测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import WorkflowEngine

def test_workflow_engine():
    engine = WorkflowEngine()

    # 测试步骤定义
    engine.add_step("step1", lambda ctx: ctx.get("val", 0) + 1)
    engine.add_step("step2", lambda ctx: ctx.get("val", 0) * 2)

    # 测试顺序执行
    results = engine.run({"val": 5})
    assert results["step1"] == 6, f"step1失败: {results}"
    assert results["step2"] == 10, f"step2失败: {results}"

    # 测试条件分支
    engine2 = WorkflowEngine()
    engine2.add_step("conditional", lambda ctx: "executed", condition=lambda ctx: ctx.get("run", False))
    assert "conditional" not in engine2.run({"run": False})
    assert engine2.run({"run": True})["conditional"] == "executed"

    # 测试并行执行
    engine3 = WorkflowEngine()
    engine3.add_step("a", lambda ctx: 1, parallel=True)
    engine3.add_step("b", lambda ctx: 2, parallel=True)
    results = engine3.run_parallel({})
    assert results["a"] == 1
    assert results["b"] == 2

    print("✅ 阶段52 工作流引擎测试通过")

if __name__ == "__main__":
    test_workflow_engine()
