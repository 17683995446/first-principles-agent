#!/usr/bin/env python3
"""
阶段23测试：验证数据备份和恢复
"""
import sys
import os
import shutil

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from first_principles_agent import FirstPrincipleKG

print("=" * 60)
print("阶段23测试：数据备份和恢复")
print("=" * 60)

# 清理测试目录
test_backup_dir = "test_backups"
if os.path.exists(test_backup_dir):
    shutil.rmtree(test_backup_dir)

# 测试1：验证创建备份
print("\n[测试1] 验证创建备份")
try:
    kg = FirstPrincipleKG()
    
    # 添加测试数据
    kg.add_node("备份测试节点", {"type": "test"})
    kg.add_edge("节点A", "节点B", "测试关系", weight=0.9)
    
    # 创建备份
    backup_path = kg.create_backup(test_backup_dir)
    
    if backup_path and os.path.exists(backup_path):
        print("✅ 备份创建成功")
        print(f"   备份路径: {backup_path}")
        print(f"   文件大小: {os.path.getsize(backup_path)} 字节")
    else:
        print("❌ 备份创建失败")
except Exception as e:
    print(f"❌ 备份创建测试失败: {e}")
    import traceback
    traceback.print_exc()

# 测试2：验证列出备份
print("\n[测试2] 验证列出备份")
try:
    backups = kg.list_backups(test_backup_dir)
    
    if len(backups) > 0:
        print("✅ 备份列表获取成功")
        print(f"   备份数量: {len(backups)}")
        for backup in backups:
            print(f"   - {backup['filename']} ({backup['size']} 字节)")
    else:
        print("❌ 备份列表为空")
except Exception as e:
    print(f"❌ 列出备份测试失败: {e}")

# 测试3：验证恢复备份
print("\n[测试3] 验证恢复备份")
try:
    # 修改当前图谱
    kg.add_node("新节点", {"type": "new"})
    original_nodes = len(kg.graph["nodes"])
    print(f"   修改后节点数: {original_nodes}")
    
    # 从备份恢复
    if backups:
        success = kg.restore_from_backup(backups[0]["path"])
        
        if success:
            restored_nodes = len(kg.graph["nodes"])
            print(f"   恢复后节点数: {restored_nodes}")
            
            if restored_nodes < original_nodes:
                print("✅ 备份恢复成功（节点数减少，说明恢复到了备份状态）")
            else:
                print("⚠️ 备份恢复可能未生效")
        else:
            print("❌ 备份恢复失败")
    else:
        print("⚠️ 没有可用备份进行恢复测试")
except Exception as e:
    print(f"❌ 备份恢复测试失败: {e}")
    import traceback
    traceback.print_exc()

# 测试4：验证向后兼容
print("\n[测试4] 验证向后兼容")
try:
    kg = FirstPrincipleKG()
    kg.add_node("兼容测试")
    insights = kg.get_insights()
    print("✅ 向后兼容检查通过")
    print(f"   节点数: {insights['total_nodes']}")
except Exception as e:
    print(f"❌ 向后兼容测试失败: {e}")

# 清理测试目录
if os.path.exists(test_backup_dir):
    shutil.rmtree(test_backup_dir)

print("\n" + "=" * 60)
print("阶段23测试完成！")
print("=" * 60)
