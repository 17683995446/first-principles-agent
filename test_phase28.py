#!/usr/bin/env python3
"""
阶段28测试：验证数据验证器（DataValidator类）
"""
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from first_principles_agent import DataValidator, FirstPrincipleKG, FirstPrincipleEternalAgent

print("=" * 60)
print("阶段28测试：数据验证器（DataValidator类）")
print("=" * 60)

# 测试1：验证DataValidator初始化
print("\n[测试1] 验证DataValidator初始化")
try:
    validator = DataValidator()
    assert validator.custom_rules is not None
    print("✅ DataValidator初始化成功")
except Exception as e:
    print(f"❌ DataValidator初始化失败: {e}")

# 测试2：验证节点数据格式
print("\n[测试2] 验证节点数据格式")
try:
    validator = DataValidator()

    # 有效节点
    result = validator.validate_node("测试节点", {"type": "concept"})
    assert result["valid"] is True
    assert len(result["errors"]) == 0
    print("✅ 有效节点验证通过")

    # 空名称
    result = validator.validate_node("")
    assert result["valid"] is False
    assert "节点名称不能为空" in result["errors"]
    print("✅ 空名称节点验证失败（符合预期）")

    # 非字符串名称
    result = validator.validate_node(123)
    assert result["valid"] is False
    assert "节点名称必须是字符串" in result["errors"]
    print("✅ 非字符串名称验证失败（符合预期）")

    # 名称过长
    result = validator.validate_node("x" * 201)
    assert result["valid"] is False
    assert "节点名称长度不能超过200" in result["errors"]
    print("✅ 过长名称验证失败（符合预期）")

except Exception as e:
    print(f"❌ 节点验证测试失败: {e}")

# 测试3：验证边数据格式
print("\n[测试3] 验证边数据格式")
try:
    validator = DataValidator()

    # 有效边
    result = validator.validate_edge("节点A", "节点B", "关联", 0.8)
    assert result["valid"] is True
    print("✅ 有效边验证通过")

    # 无效源节点
    result = validator.validate_edge("", "节点B", "关联")
    assert result["valid"] is False
    assert "边的源节点必须是有效的字符串" in result["errors"]
    print("✅ 无效源节点验证失败（符合预期）")

    # 权重超出范围
    result = validator.validate_edge("节点A", "节点B", "关联", 1.5)
    assert result["valid"] is False
    assert "边的权重必须在0.0到1.0之间" in result["errors"]
    print("✅ 权重超出范围验证失败（符合预期）")

    # 非数字权重
    result = validator.validate_edge("节点A", "节点B", "关联", "heavy")
    assert result["valid"] is False
    assert "边的权重必须是数字" in result["errors"]
    print("✅ 非数字权重验证失败（符合预期）")

except Exception as e:
    print(f"❌ 边验证测试失败: {e}")

# 测试4：验证任务数据格式
print("\n[测试4] 验证任务数据格式")
try:
    validator = DataValidator()

    # 有效任务
    result = validator.validate_task("执行任务A")
    assert result["valid"] is True
    print("✅ 有效任务验证通过")

    # 空任务
    result = validator.validate_task("")
    assert result["valid"] is False
    assert "任务不能为空" in result["errors"]
    print("✅ 空任务验证失败（符合预期）")

    # 非字符串任务
    result = validator.validate_task(123)
    assert result["valid"] is False
    assert "任务必须是字符串" in result["errors"]
    print("✅ 非字符串任务验证失败（符合预期）")

except Exception as e:
    print(f"❌ 任务验证测试失败: {e}")

# 测试5：验证自定义验证规则
print("\n[测试5] 验证自定义验证规则")
try:
    validator = DataValidator()

    def must_start_with_hello(data):
        return isinstance(data, str) and data.startswith("Hello")

    validator.add_custom_rule("hello_rule", must_start_with_hello)

    result = validator.validate_with_custom("Hello World", "hello_rule")
    assert result["valid"] is True
    print("✅ 自定义规则验证通过")

    result = validator.validate_with_custom("World", "hello_rule")
    assert result["valid"] is False
    print("✅ 自定义规则验证失败（符合预期）")

    # 不存在的规则
    result = validator.validate_with_custom("test", "nonexistent")
    assert result["valid"] is False
    assert "不存在" in result["errors"][0]
    print("✅ 不存在规则验证失败（符合预期）")

except Exception as e:
    print(f"❌ 自定义规则测试失败: {e}")

# 测试6：验证统一验证入口
print("\n[测试6] 验证统一验证入口")
try:
    validator = DataValidator()

    result = validator.validate_all(
        name="节点1",
        attr={"type": "concept"},
        source="A",
        target="B",
        relation="关联",
        weight=0.5,
        task="任务1"
    )

    assert "node" in result
    assert "edge" in result
    assert "task" in result
    assert result["node"]["valid"] is True
    assert result["edge"]["valid"] is True
    assert result["task"]["valid"] is True
    print("✅ 统一验证入口正常")
except Exception as e:
    print(f"❌ 统一验证入口测试失败: {e}")

# 测试7：验证集成到FirstPrincipleKG
print("\n[测试7] 验证集成到FirstPrincipleKG")
try:
    kg = FirstPrincipleKG()
    assert hasattr(kg, 'validator')
    assert kg.validator is not None
    assert isinstance(kg.validator, DataValidator)
    print("✅ FirstPrincipleKG集成DataValidator成功")
    print(f"   validator类型: {type(kg.validator).__name__}")
except Exception as e:
    print(f"❌ FirstPrincipleKG集成测试失败: {e}")

# 测试8：验证集成到FirstPrincipleEternalAgent（通过kg间接集成）
print("\n[测试8] 验证通过Agent访问验证器")
try:
    agent = FirstPrincipleEternalAgent()
    assert hasattr(agent.kg, 'validator')
    result = agent.kg.validator.validate_node("测试")
    assert result["valid"] is True
    print("✅ 通过Agent访问验证器成功")
except Exception as e:
    print(f"❌ Agent访问验证器测试失败: {e}")

# 测试9：验证自定义规则返回字典
print("\n[测试9] 验证自定义规则返回字典")
try:
    validator = DataValidator()

    def dict_rule(data):
        return {"valid": data > 10, "errors": [] if data > 10 else ["必须大于10"]}

    validator.add_custom_rule("gt10", dict_rule)
    result = validator.validate_with_custom(15, "gt10")
    assert result["valid"] is True
    result = validator.validate_with_custom(5, "gt10")
    assert result["valid"] is False
    print("✅ 自定义规则返回字典测试通过")
except Exception as e:
    print(f"❌ 自定义规则返回字典测试失败: {e}")

# 测试10：验证属性类型错误
print("\n[测试10] 验证属性类型错误")
try:
    validator = DataValidator()
    result = validator.validate_node("节点", attr="invalid")
    assert result["valid"] is False
    assert "节点属性必须是字典" in result["errors"]
    print("✅ 属性类型错误验证通过")
except Exception as e:
    print(f"❌ 属性类型错误测试失败: {e}")

print("\n" + "=" * 60)
print("阶段28测试完成！")
print("=" * 60)
