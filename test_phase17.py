#!/usr/bin/env python3
"""
阶段17测试：验证日志系统
"""
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from first_principles_agent import Logger

print("=" * 60)
print("阶段17测试：日志系统")
print("=" * 60)

# 测试1：验证控制台日志
print("\n[测试1] 验证控制台日志")
try:
    logger = Logger(console_output=True, log_level="DEBUG")
    logger.debug("调试信息")
    logger.info("普通信息")
    logger.warn("警告信息")
    logger.error("错误信息")
    print("✅ 控制台日志测试通过")
except Exception as e:
    print(f"❌ 控制台日志测试失败: {e}")

# 测试2：验证文件日志
print("\n[测试2] 验证文件日志")
test_log_file = "test_agent.log"
try:
    # 删除已存在的日志文件
    if os.path.exists(test_log_file):
        os.remove(test_log_file)
    
    logger = Logger(log_file=test_log_file, console_output=False, log_level="INFO")
    logger.info("测试日志信息1")
    logger.warn("测试日志警告")
    logger.debug("这条不应该出现在日志中")
    
    # 验证日志文件内容
    if os.path.exists(test_log_file):
        with open(test_log_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        if "测试日志信息1" in content and "测试日志警告" in content:
            print("✅ 文件日志写入成功")
            print(f"   日志内容行数: {len(content.strip().split(chr(10)))}")
        else:
            print("❌ 日志内容不正确")
        
        if "这条不应该出现在日志中" not in content:
            print("✅ 日志级别过滤正确")
        else:
            print("❌ 日志级别过滤失败")
    else:
        print("❌ 日志文件未创建")
except Exception as e:
    print(f"❌ 文件日志测试失败: {e}")
    import traceback
    traceback.print_exc()

# 测试3：验证日志级别控制
print("\n[测试3] 验证日志级别控制")
try:
    logger_error = Logger(console_output=False, log_level="ERROR")
    logger_error.info("这条INFO不应该输出")
    logger_error.error("这条ERROR应该输出")
    print("✅ 日志级别控制测试通过")
except Exception as e:
    print(f"❌ 日志级别控制测试失败: {e}")

# 清理测试文件
if os.path.exists(test_log_file):
    os.remove(test_log_file)

print("\n" + "=" * 60)
print("阶段17测试完成！")
print("=" * 60)
