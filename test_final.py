#!/usr/bin/env python3
"""最终测试：所有改进一起运行"""
import sys
import time
import signal

# 修改配置以加快测试
sys.path.insert(0, '/workspace')

from first_principles_agent import (
    FirstPrincipleEternalAgent,
    TASK_POOL,
    SAVE_EVERY_N,
    EVOLVE_CYCLE,
    LLM_DEMO_MODE,
    LOOP_SLEEP
)

# 配置
LLM_DEMO_MODE = True
original_loop_sleep = LOOP_SLEEP
LOOP_SLEEP = 0.01

class TimeoutHandler:
    """超时处理"""
    def __init__(self, timeout=3):
        self.timeout = timeout
        self.agent = None
    
    def handler(self, signum, frame):
        print("\n\n⏱️  测试时间到！")
        if self.agent:
            self.agent.shutdown()
        sys.exit(0)

def test_all_improvements():
    """测试所有改进一起运行"""
    print("╔" + "═" * 58 + "╗")
    print("║  🚀 最终测试：所有阶段改进一起运行  ║")
    print("╚" + "═" * 58 + "╝")
    
    agent = FirstPrincipleEternalAgent()
    
    # 清空现有任务
    while TASK_POOL:
        TASK_POOL.popleft()
    
    # 添加一些测试任务
    TASK_POOL.append("探索:第一性原理")
    TASK_POOL.append("优化:知识图谱")
    TASK_POOL.append("测试:所有改进")
    
    timeout_handler = TimeoutHandler(timeout=3)
    timeout_handler.agent = agent
    
    # 设置定时器
    signal.signal(signal.SIGALRM, timeout_handler.handler)
    signal.alarm(timeout_handler.timeout)
    
    print(f"\n📝 开始运行 {timeout_handler.timeout} 秒...")
    print("-" * 60)
    
    try:
        agent.eternal_loop()
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 恢复原始配置
        global LOOP_SLEEP
        LOOP_SLEEP = original_loop_sleep

if __name__ == "__main__":
    test_all_improvements()
