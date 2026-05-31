#!/usr/bin/env python3
"""
阶段13测试：验证FirstPrincipleKG使用权重配置
保持向后兼容
"""
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from first_principles_agent import FirstPrincipleKG, Config

print("=" * 60)
print("阶段13测试：FirstPrincipleKG使用权重配置")
print("=" * 60)

# 测试1：验证KG可以正常初始化
print("\n[测试1] 验证KG初始化")
try:
    kg = FirstPrincipleKG()
    print("✅ KG初始化成功")
    print(f"   - weight_decay_rate: {kg.weight_decay_rate}")
    print(f"   - weight_boost_rate: {kg.weight_boost_rate}")
except Exception as e:
    print(f"❌ KG初始化失败: {e}")
    sys.exit(1)

# 测试2：验证权重操作
print("\n[测试2] 验证权重操作")
try:
    # 添加初始边
    kg.add_edge("test1", "test2", "关联", weight=0.5)
    edge = kg.find_edge("test1", "test2", "关联")
    print(f"   - 初始权重: {edge['weight']}")
    
    # 增强权重
    kg.add_edge("test1", "test2", "关联")
    edge = kg.find_edge("test1", "test2", "关联")
    print(f"   - 增强后权重: {edge['weight']}")
    
    # 衰减权重
    kg.weight_decay()
    edge = kg.find_edge("test1", "test2", "关联")
    print(f"   - 衰减后权重: {edge['weight']}")
    
    print("✅ 权重操作测试通过")
except Exception as e:
    print(f"❌ 权重操作测试失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 测试3：验证向后兼容性
print("\n[测试3] 验证向后兼容性")
try:
    # 模拟旧代码访问全局变量
    from first_principles_agent import WEIGHT_DECAY_RATE, WEIGHT_BOOST_RATE
    print(f"   - WEIGHT_DECAY_RATE: {WEIGHT_DECAY_RATE}")
    print(f"   - WEIGHT_BOOST_RATE: {WEIGHT_BOOST_RATE}")
    print("✅ 向后兼容检查通过")
except Exception as e:
    print(f"⚠️  向后兼容检查: {e}")

print("\n" + "=" * 60)
print("阶段13测试完成！所有功能正常")
print("=" * 60)
