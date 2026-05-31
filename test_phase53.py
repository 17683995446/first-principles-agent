"""阶段53：规则引擎测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import RuleEngine

def test_rule_engine():
    engine = RuleEngine()

    # 测试规则定义
    engine.add_rule("high_temp", lambda f: f.get("temp", 0) > 30, lambda f: "cooling", priority=1)
    engine.add_rule("low_temp", lambda f: f.get("temp", 0) < 10, lambda f: "heating", priority=2)

    # 测试规则匹配
    triggered = engine.evaluate({"temp": 35})
    assert len(triggered) == 1
    assert triggered[0]["name"] == "high_temp"

    # 测试规则执行
    results = engine.execute({"temp": 35})
    assert results[0]["result"] == "cooling"

    # 测试无匹配
    assert len(engine.evaluate({"temp": 20})) == 0

    # 测试规则列表
    assert "high_temp" in engine.get_rules()
    assert "low_temp" in engine.get_rules()

    print("✅ 阶段53 规则引擎测试通过")

if __name__ == "__main__":
    test_rule_engine()
