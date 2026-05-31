#!/usr/bin/env python3
"""
阶段30测试：验证健康检查端点（HealthCheck类）
"""
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from first_principles_agent import HealthCheck, APIWrapper, FirstPrincipleEternalAgent

print("=" * 60)
print("阶段30测试：健康检查端点（HealthCheck类）")
print("=" * 60)

# 测试1：验证HealthCheck初始化
print("\n[测试1] 验证HealthCheck初始化")
try:
    hc = HealthCheck()
    assert hc.checks == {}
    assert hc.agent is None
    print("✅ HealthCheck初始化成功")
except Exception as e:
    print(f"❌ HealthCheck初始化失败: {e}")

# 测试2：验证注册健康检查项
print("\n[测试2] 验证注册健康检查项")
try:
    hc = HealthCheck()

    def check_memory():
        return {"healthy": True, "usage": "50%"}

    hc.register_check("memory", check_memory)
    assert "memory" in hc.checks
    print("✅ 健康检查项注册成功")
except Exception as e:
    print(f"❌ 健康检查项注册失败: {e}")

# 测试3：验证单个组件检查
print("\n[测试3] 验证单个组件检查")
try:
    hc = HealthCheck()

    def check_cpu():
        return {"healthy": True, "load": 0.5}

    hc.register_check("cpu", check_cpu)
    result = hc.check_component("cpu")
    assert result["healthy"] is True
    assert result["name"] == "cpu"
    assert result["load"] == 0.5
    print("✅ 单个组件检查正常")
    print(f"   检查结果: {result}")
except Exception as e:
    print(f"❌ 单个组件检查失败: {e}")

# 测试4：验证未注册组件检查
print("\n[测试4] 验证未注册组件检查")
try:
    hc = HealthCheck()
    result = hc.check_component("unknown")
    assert result["healthy"] is False
    assert "未注册" in result["error"]
    print("✅ 未注册组件检查失败（符合预期）")
except Exception as e:
    print(f"❌ 未注册组件检查测试失败: {e}")

# 测试5：验证异常处理
print("\n[测试5] 验证异常处理")
try:
    hc = HealthCheck()

    def bad_check():
        raise RuntimeError("检查异常")

    hc.register_check("bad", bad_check)
    result = hc.check_component("bad")
    assert result["healthy"] is False
    assert "检查异常" in result["error"]
    print("✅ 异常处理正常")
except Exception as e:
    print(f"❌ 异常处理测试失败: {e}")

# 测试6：验证健康报告生成
print("\n[测试6] 验证健康报告生成")
try:
    hc = HealthCheck()

    def check_a():
        return True

    def check_b():
        return False

    hc.register_check("a", check_a)
    hc.register_check("b", check_b)
    report = hc.get_health_report()
    assert report["status"] == "unhealthy"
    assert report["summary"]["total"] == 2
    assert report["summary"]["healthy"] == 1
    assert report["summary"]["unhealthy"] == 1
    assert "timestamp" in report
    assert "checks" in report
    print("✅ 健康报告生成正常")
    print(f"   状态: {report['status']}")
    print(f"   摘要: {report['summary']}")
except Exception as e:
    print(f"❌ 健康报告生成失败: {e}")

# 测试7：验证全部健康的报告
print("\n[测试7] 验证全部健康的报告")
try:
    hc = HealthCheck()

    def check_ok():
        return True

    hc.register_check("ok1", check_ok)
    hc.register_check("ok2", check_ok)
    report = hc.get_health_report()
    assert report["status"] == "healthy"
    assert report["summary"]["healthy"] == 2
    print("✅ 全部健康报告正常")
except Exception as e:
    print(f"❌ 全部健康报告测试失败: {e}")

# 测试8：验证集成到APIWrapper
print("\n[测试8] 验证集成到APIWrapper")
try:
    agent = FirstPrincipleEternalAgent()
    api = APIWrapper(agent)
    assert hasattr(api, 'health_check')
    assert api.health_check is not None
    assert isinstance(api.health_check, HealthCheck)
    print("✅ APIWrapper集成HealthCheck成功")
    print(f"   health_check类型: {type(api.health_check).__name__}")
except Exception as e:
    print(f"❌ APIWrapper集成测试失败: {e}")

# 测试9：验证健康检查API路由
print("\n[测试9] 验证健康检查API路由")
try:
    agent = FirstPrincipleEternalAgent()
    result = agent.api.handle_request("GET", "/health")
    assert result.get("status") in (200, 503)
    assert "summary" in result
    assert "checks" in result
    print("✅ 健康检查API路由正常")
    print(f"   状态码: {result['status']}")
    print(f"   摘要: {result['summary']}")
except Exception as e:
    print(f"❌ 健康检查API路由测试失败: {e}")

# 测试10：验证Agent状态检查
print("\n[测试10] 验证Agent状态检查")
try:
    agent = FirstPrincipleEternalAgent()
    hc = HealthCheck(agent)
    result = hc.check_agent()
    assert result["healthy"] is True
    assert "run_count" in result
    assert "uptime" in result
    print("✅ Agent状态检查正常")
    print(f"   结果: {result}")
except Exception as e:
    print(f"❌ Agent状态检查失败: {e}")

# 测试11：验证知识图谱状态检查
print("\n[测试11] 验证知识图谱状态检查")
try:
    agent = FirstPrincipleEternalAgent()
    hc = HealthCheck(agent)
    result = hc.check_kg()
    assert result["healthy"] is True
    assert "nodes" in result
    assert "edges" in result
    print("✅ 知识图谱状态检查正常")
    print(f"   结果: {result}")
except Exception as e:
    print(f"❌ 知识图谱状态检查失败: {e}")

# 测试12：验证API状态检查
print("\n[测试12] 验证API状态检查")
try:
    agent = FirstPrincipleEternalAgent()
    hc = HealthCheck(agent)
    result = hc.check_api()
    assert result["healthy"] is True
    assert "routes" in result
    print("✅ API状态检查正常")
    print(f"   结果: {result}")
except Exception as e:
    print(f"❌ API状态检查失败: {e}")

# 测试13：验证默认检查项注册
print("\n[测试13] 验证默认检查项注册")
try:
    agent = FirstPrincipleEternalAgent()
    api = APIWrapper(agent)
    default_checks = ["agent", "kg", "api"]
    for name in default_checks:
        assert name in api.health_check.checks, f"默认检查项 {name} 未注册"
    print("✅ 默认检查项注册正常")
    print(f"   已注册: {list(api.health_check.checks.keys())}")
except Exception as e:
    print(f"❌ 默认检查项注册测试失败: {e}")

print("\n" + "=" * 60)
print("阶段30测试完成！")
print("=" * 60)
