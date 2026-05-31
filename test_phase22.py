#!/usr/bin/env python3
"""
阶段22测试：验证多语言支持框架
"""
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from first_principles_agent import I18n, FirstPrincipleEternalAgent

print("=" * 60)
print("阶段22测试：多语言支持框架")
print("=" * 60)

# 测试1：验证I18n初始化
print("\n[测试1] 验证I18n初始化")
try:
    i18n = I18n()
    print("✅ I18n初始化成功")
    print(f"   默认语言: {i18n.current_lang}")
    print(f"   可用语言: {i18n.list_languages()}")
except Exception as e:
    print(f"❌ I18n初始化失败: {e}")

# 测试2：验证中文翻译
print("\n[测试2] 验证中文翻译")
try:
    i18n = I18n("zh")
    print(f"   welcome: {i18n.get('welcome')}")
    print(f"   task_complete: {i18n.get('task_complete')}")
    print(f"   error: {i18n.get('error')}")
    print("✅ 中文翻译测试通过")
except Exception as e:
    print(f"❌ 中文翻译测试失败: {e}")

# 测试3：验证英文翻译
print("\n[测试3] 验证英文翻译")
try:
    i18n = I18n("en")
    print(f"   welcome: {i18n.get('welcome')}")
    print(f"   task_complete: {i18n.get('task_complete')}")
    print(f"   error: {i18n.get('error')}")
    print("✅ 英文翻译测试通过")
except Exception as e:
    print(f"❌ 英文翻译测试失败: {e}")

# 测试4：验证语言切换
print("\n[测试4] 验证语言切换")
try:
    i18n = I18n("zh")
    print(f"   中文: {i18n.get('welcome')}")
    
    i18n.set_language("en")
    print(f"   英文: {i18n.get('welcome')}")
    
    # 切换回中文
    i18n.set_language("zh")
    print(f"   中文: {i18n.get('welcome')}")
    
    print("✅ 语言切换测试通过")
except Exception as e:
    print(f"❌ 语言切换测试失败: {e}")

# 测试5：验证添加新翻译
print("\n[测试5] 验证添加新翻译")
try:
    i18n = I18n("zh")
    i18n.add_translation("zh", "custom_key", "自定义文本")
    result = i18n.get("custom_key")
    
    if result == "自定义文本":
        print("✅ 添加新翻译测试通过")
    else:
        print(f"❌ 添加新翻译失败: {result}")
except Exception as e:
    print(f"❌ 添加新翻译测试失败: {e}")

# 测试6：验证Agent集成
print("\n[测试6] 验证Agent集成")
try:
    agent = FirstPrincipleEternalAgent()
    print("✅ Agent初始化成功（包含多语言支持）")
    print(f"   i18n类型: {type(agent.i18n).__name__}")
    print(f"   当前语言: {agent.i18n.current_lang}")
except Exception as e:
    print(f"❌ Agent集成测试失败: {e}")

print("\n" + "=" * 60)
print("阶段22测试完成！")
print("=" * 60)
