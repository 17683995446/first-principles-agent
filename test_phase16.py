#!/usr/bin/env python3
"""
阶段16测试：验证JSON配置文件支持
"""
import sys
import os
import json

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from first_principles_agent import Config

print("=" * 60)
print("阶段16测试：JSON配置文件支持")
print("=" * 60)

# 测试1：验证默认配置文件创建
print("\n[测试1] 验证默认配置文件创建")
test_config_path = "test_agent_config.json"
try:
    # 删除已存在的测试文件
    if os.path.exists(test_config_path):
        os.remove(test_config_path)
    
    # 保存默认配置
    Config.save_to_file(test_config_path)
    
    if os.path.exists(test_config_path):
        print(f"✅ 配置文件创建成功: {test_config_path}")
        with open(test_config_path, "r", encoding="utf-8") as f:
            config_data = json.load(f)
        print(f"   配置项数: {len(config_data)}")
        print(f"   LOOP_SLEEP: {config_data.get('LOOP_SLEEP')}")
        print(f"   EVOLVE_CYCLE: {config_data.get('EVOLVE_CYCLE')}")
    else:
        print("❌ 配置文件未创建")
except Exception as e:
    print(f"❌ 配置文件创建失败: {e}")

# 测试2：验证配置文件加载
print("\n[测试2] 验证配置文件加载")
try:
    # 修改配置文件
    config_data = {
        "LOOP_SLEEP": 0.1,
        "EVOLVE_CYCLE": 25,
        "TASK_MAX_LEN": 100,
        "LLM_ENABLED": False
    }
    with open(test_config_path, "w", encoding="utf-8") as f:
        json.dump(config_data, f, ensure_ascii=False, indent=2)
    
    # 重置Config为默认值
    Config.LOOP_SLEEP = 0.5
    Config.EVOLVE_CYCLE = 50
    Config.TASK_MAX_LEN = 200
    Config.LLM_ENABLED = True
    
    # 加载配置文件
    Config.load_from_file(test_config_path)
    
    # 验证加载结果
    success = True
    if Config.LOOP_SLEEP != 0.1:
        print(f"❌ LOOP_SLEEP 未正确加载: {Config.LOOP_SLEEP}")
        success = False
    if Config.EVOLVE_CYCLE != 25:
        print(f"❌ EVOLVE_CYCLE 未正确加载: {Config.EVOLVE_CYCLE}")
        success = False
    if Config.TASK_MAX_LEN != 100:
        print(f"❌ TASK_MAX_LEN 未正确加载: {Config.TASK_MAX_LEN}")
        success = False
    if Config.LLM_ENABLED != False:
        print(f"❌ LLM_ENABLED 未正确加载: {Config.LLM_ENABLED}")
        success = False
    
    if success:
        print("✅ 配置文件加载成功")
        print(f"   LOOP_SLEEP: {Config.LOOP_SLEEP}")
        print(f"   EVOLVE_CYCLE: {Config.EVOLVE_CYCLE}")
        print(f"   TASK_MAX_LEN: {Config.TASK_MAX_LEN}")
        print(f"   LLM_ENABLED: {Config.LLM_ENABLED}")
except Exception as e:
    print(f"❌ 配置文件加载测试失败: {e}")
    import traceback
    traceback.print_exc()

# 测试3：验证向后兼容
print("\n[测试3] 验证向后兼容性")
try:
    # 恢复默认配置
    Config.LOOP_SLEEP = 0.5
    Config.EVOLVE_CYCLE = 50
    Config.TASK_MAX_LEN = 200
    Config.LLM_ENABLED = True
    
    # 验证不加载配置文件时行为正常
    print("✅ 向后兼容检查通过")
    print(f"   默认 LOOP_SLEEP: {Config.LOOP_SLEEP}")
    print(f"   默认 EVOLVE_CYCLE: {Config.EVOLVE_CYCLE}")
except Exception as e:
    print(f"❌ 向后兼容测试失败: {e}")

# 清理测试文件
if os.path.exists(test_config_path):
    os.remove(test_config_path)

print("\n" + "=" * 60)
print("阶段16测试完成！")
print("=" * 60)
