#!/usr/bin/env python3
"""
阶段47测试：验证数据库接口（DatabaseInterface类）
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from first_principles_agent import DatabaseInterface

print("=" * 60)
print("阶段47测试：数据库接口（DatabaseInterface类）")
print("=" * 60)

# 测试1：验证DatabaseInterface初始化
print("\n[测试1] 验证DatabaseInterface初始化")
try:
    db = DatabaseInterface(":memory:")
    assert db.db_path == ":memory:"
    print("✅ DatabaseInterface初始化成功")
except Exception as e:
    print(f"❌ DatabaseInterface初始化失败: {e}")

# 测试2：验证create_table
print("\n[测试2] 验证create_table")
try:
    db = DatabaseInterface(":memory:")
    db.create_table("users", {"id": "INTEGER PRIMARY KEY", "name": "TEXT", "age": "INTEGER"})
    print("✅ create_table正常")
except Exception as e:
    print(f"❌ create_table测试失败: {e}")

# 测试3：验证insert
print("\n[测试3] 验证insert")
try:
    db = DatabaseInterface(":memory:")
    db.create_table("users", {"id": "INTEGER PRIMARY KEY", "name": "TEXT", "age": "INTEGER"})
    db.insert("users", {"id": 1, "name": "Alice", "age": 30})
    db.insert("users", {"id": 2, "name": "Bob", "age": 25})
    print("✅ insert正常")
except Exception as e:
    print(f"❌ insert测试失败: {e}")

# 测试4：验证select
print("\n[测试4] 验证select")
try:
    db = DatabaseInterface(":memory:")
    db.create_table("users", {"id": "INTEGER PRIMARY KEY", "name": "TEXT", "age": "INTEGER"})
    db.insert("users", {"id": 1, "name": "Alice", "age": 30})
    result = db.select("users")
    assert len(result) == 1
    assert result[0][1] == "Alice"
    print(f"✅ select正常: {result}")
except Exception as e:
    print(f"❌ select测试失败: {e}")

# 测试5：验证select带where
print("\n[测试5] 验证select带where")
try:
    db = DatabaseInterface(":memory:")
    db.create_table("users", {"id": "INTEGER PRIMARY KEY", "name": "TEXT", "age": "INTEGER"})
    db.insert("users", {"id": 1, "name": "Alice", "age": 30})
    db.insert("users", {"id": 2, "name": "Bob", "age": 25})
    result = db.select("users", "age > ?", (25,))
    assert len(result) == 1
    assert result[0][1] == "Alice"
    print(f"✅ select带where正常: {result}")
except Exception as e:
    print(f"❌ select带where测试失败: {e}")

# 测试6：验证update
print("\n[测试6] 验证update")
try:
    db = DatabaseInterface(":memory:")
    db.create_table("users", {"id": "INTEGER PRIMARY KEY", "name": "TEXT", "age": "INTEGER"})
    db.insert("users", {"id": 1, "name": "Alice", "age": 30})
    db.update("users", {"age": 31}, "id = ?", (1,))
    result = db.select("users", "id = 1")
    assert result[0][2] == 31
    print("✅ update正常")
except Exception as e:
    print(f"❌ update测试失败: {e}")

# 测试7：验证delete
print("\n[测试7] 验证delete")
try:
    db = DatabaseInterface(":memory:")
    db.create_table("users", {"id": "INTEGER PRIMARY KEY", "name": "TEXT", "age": "INTEGER"})
    db.insert("users", {"id": 1, "name": "Alice", "age": 30})
    db.insert("users", {"id": 2, "name": "Bob", "age": 25})
    db.delete("users", "id = ?", (1,))
    result = db.select("users")
    assert len(result) == 1
    assert result[0][1] == "Bob"
    print("✅ delete正常")
except Exception as e:
    print(f"❌ delete测试失败: {e}")

# 测试8：验证fetchone
print("\n[测试8] 验证fetchone")
try:
    db = DatabaseInterface(":memory:")
    db.create_table("users", {"id": "INTEGER PRIMARY KEY", "name": "TEXT"})
    db.insert("users", {"id": 1, "name": "Alice"})
    result = db.fetchone("SELECT * FROM users WHERE id = ?", (1,))
    assert result is not None
    assert result[1] == "Alice"
    print(f"✅ fetchone正常: {result}")
except Exception as e:
    print(f"❌ fetchone测试失败: {e}")

# 测试9：验证execute
print("\n[测试9] 验证execute")
try:
    db = DatabaseInterface(":memory:")
    cursor = db.execute("SELECT 1 + 1")
    result = cursor.fetchone()
    assert result[0] == 2
    print("✅ execute正常")
except Exception as e:
    print(f"❌ execute测试失败: {e}")

# 测试10：验证连接池
print("\n[测试10] 验证连接池")
try:
    db = DatabaseInterface(":memory:")
    assert len(db._pool) == db._pool_size
    print(f"✅ 连接池正常: 大小={len(db._pool)}")
except Exception as e:
    print(f"❌ 连接池测试失败: {e}")

# 测试11：验证close
print("\n[测试11] 验证close")
try:
    db = DatabaseInterface(":memory:")
    db.close()
    assert len(db._pool) == 0
    print("✅ close正常")
except Exception as e:
    print(f"❌ close测试失败: {e}")

# 测试12：验证多表操作
print("\n[测试12] 验证多表操作")
try:
    db = DatabaseInterface(":memory:")
    db.create_table("t1", {"id": "INTEGER", "val": "TEXT"})
    db.create_table("t2", {"id": "INTEGER", "val": "TEXT"})
    db.insert("t1", {"id": 1, "val": "a"})
    db.insert("t2", {"id": 1, "val": "b"})
    r1 = db.select("t1")
    r2 = db.select("t2")
    assert len(r1) == 1
    assert len(r2) == 1
    print("✅ 多表操作正常")
except Exception as e:
    print(f"❌ 多表操作测试失败: {e}")

print("\n" + "=" * 60)
print("阶段47测试完成！")
print("=" * 60)
