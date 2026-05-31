"""汇总测试：运行阶段51-75的所有测试"""
import sys
import os
import importlib
import traceback

sys.path.insert(0, '/workspace')

# 禁用Agent启动时的输出
os.environ['CI'] = 'true'

test_modules = []
for i in range(51, 76):
    module_name = f"test_phase{i}"
    try:
        mod = importlib.import_module(module_name)
        test_modules.append((i, mod))
    except Exception as e:
        print(f"❌ 阶段{i}: 导入失败 - {e}")

results = []
for phase, mod in test_modules:
    # 查找测试函数
    test_func = None
    for name in dir(mod):
        if name.startswith('test_'):
            test_func = getattr(mod, name)
            break

    if test_func is None:
        results.append((phase, False, "未找到测试函数"))
        continue

    try:
        test_func()
        results.append((phase, True, "通过"))
    except AssertionError as e:
        results.append((phase, False, f"断言失败: {e}"))
    except Exception as e:
        results.append((phase, False, f"异常: {type(e).__name__}: {e}"))

print("\n" + "=" * 60)
print("阶段51-75 测试结果汇总")
print("=" * 60)

passed = 0
failed = 0
for phase, success, msg in results:
    status = "✅ 通过" if success else "❌ 失败"
    if success:
        passed += 1
        print(f"阶段{phase:2d}: {status}")
    else:
        failed += 1
        print(f"阶段{phase:2d}: {status} - {msg}")

print("=" * 60)
print(f"总计: {passed} 通过, {failed} 失败, 共 {len(results)} 个阶段")
if failed == 0:
    print("🎉 所有阶段测试全部通过！")
else:
    print(f"⚠️ 有 {failed} 个阶段测试未通过")
