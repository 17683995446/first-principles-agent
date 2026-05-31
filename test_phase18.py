#!/usr/bin/env python3
"""
阶段18测试：验证性能监控和统计
"""
import sys
import os
import time

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from first_principles_agent import PerformanceMonitor, format_duration

print("=" * 60)
print("阶段18测试：性能监控和统计")
print("=" * 60)

# 测试1：验证PerformanceMonitor初始化
print("\n[测试1] 验证PerformanceMonitor初始化")
try:
    monitor = PerformanceMonitor(window_size=50)
    print("✅ PerformanceMonitor初始化成功")
    print(f"   窗口大小: {monitor.window_size}")
    print(f"   总任务数: {monitor.total_tasks}")
except Exception as e:
    print(f"❌ PerformanceMonitor初始化失败: {e}")

# 测试2：验证记录执行
print("\n[测试2] 验证记录执行")
try:
    monitor = PerformanceMonitor(window_size=10)
    
    # 模拟10次执行
    for i in range(10):
        exec_time = 50 + i * 10  # 模拟递增的执行时间
        monitor.record_execution(exec_time, success=(i != 5))  # 第6次模拟失败
    
    print("✅ 记录执行成功")
    print(f"   总任务数: {monitor.total_tasks}")
    print(f"   总错误数: {monitor.total_errors}")
except Exception as e:
    print(f"❌ 记录执行测试失败: {e}")
    import traceback
    traceback.print_exc()

# 测试3：验证统计信息
print("\n[测试3] 验证统计信息")
try:
    stats = monitor.get_stats()
    print("✅ 统计信息获取成功")
    print(f"   平均执行时间: {stats['avg_exec_time']:.2f}ms")
    print(f"   最小执行时间: {stats['min_exec_time']:.2f}ms")
    print(f"   最大执行时间: {stats['max_exec_time']:.2f}ms")
    print(f"   总任务数: {stats['total_tasks']}")
    print(f"   错误率: {stats['error_rate']:.2f}%")
    print(f"   运行时间: {format_duration(stats['uptime'])}")
except Exception as e:
    print(f"❌ 统计信息测试失败: {e}")
    import traceback
    traceback.print_exc()

# 测试4：验证性能报告
print("\n[测试4] 验证性能报告")
try:
    report = monitor.get_performance_report()
    if "性能监控报告" in report:
        print("✅ 性能报告生成成功")
        print("   报告包含关键信息")
    else:
        print("❌ 性能报告内容不正确")
except Exception as e:
    print(f"❌ 性能报告测试失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("阶段18测试完成！")
print("=" * 60)
