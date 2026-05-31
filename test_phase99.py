"""阶段99：ORM映射测试"""
import sys
import os
sys.path.insert(0, '/workspace')
from first_principles_agent import ORMMapper

def test_orm_mapper():
    db_path = "/tmp/test_orm.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    orm = ORMMapper(db_path)

    # 测试注册表
    orm.register("users", {"id": "INTEGER PRIMARY KEY", "name": "TEXT", "age": "INTEGER"})

    # 测试插入
    uid1 = orm.insert("users", {"name": "Alice", "age": 30})
    uid2 = orm.insert("users", {"name": "Bob", "age": 25})
    assert uid1 == 1
    assert uid2 == 2

    # 测试查询
    all_users = orm.select("users")
    assert len(all_users) == 2

    # 测试条件查询
    result = orm.select("users", {"name": "Alice"})
    assert len(result) == 1
    assert result[0]["age"] == 30

    # 测试更新
    orm.update("users", {"age": 31}, {"name": "Alice"})
    result = orm.select("users", {"name": "Alice"})
    assert result[0]["age"] == 31

    # 测试删除
    orm.delete("users", {"name": "Bob"})
    all_users = orm.select("users")
    assert len(all_users) == 1

    orm.close()
    os.remove(db_path)

    print("✅ 阶段99 ORM映射测试通过")

if __name__ == "__main__":
    test_orm_mapper()
