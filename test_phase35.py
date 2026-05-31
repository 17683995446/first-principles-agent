#!/usr/bin/env python3
"""
阶段35测试：验证加密器（Encryptor类）
"""
import sys
import os
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from first_principles_agent import Encryptor

print("=" * 60)
print("阶段35测试：加密器（Encryptor类）")
print("=" * 60)

# 测试1：验证Encryptor初始化
print("\n[测试1] 验证Encryptor初始化")
try:
    e = Encryptor()
    assert e.key is not None
    assert len(e.key) == 32
    print("✅ Encryptor初始化成功")
except Exception as e:
    print(f"❌ Encryptor初始化失败: {e}")

# 测试2：验证字符串加密解密
print("\n[测试2] 验证字符串加密解密")
try:
    e = Encryptor(key="my_secret_key_123")
    data = "Hello, World!"
    encrypted = e.encrypt(data)
    assert encrypted != data.encode("utf-8")
    decrypted = e.decrypt(encrypted)
    assert decrypted == data.encode("utf-8")
    print("✅ 字符串加密解密正常")
except Exception as e:
    print(f"❌ 字符串加密解密失败: {e}")

# 测试3：验证bytes加密解密
print("\n[测试3] 验证bytes加密解密")
try:
    e = Encryptor(key="test_key")
    data = b"Binary data to encrypt"
    encrypted = e.encrypt(data)
    decrypted = e.decrypt(encrypted)
    assert decrypted == data
    print("✅ bytes加密解密正常")
except Exception as e:
    print(f"❌ bytes加密解密失败: {e}")

# 测试4：验证不同密钥产生不同结果
print("\n[测试4] 验证不同密钥产生不同结果")
try:
    e1 = Encryptor(key="key1")
    e2 = Encryptor(key="key2")
    data = b"test data"
    enc1 = e1.encrypt(data)
    enc2 = e2.encrypt(data)
    assert enc1 != enc2
    print("✅ 不同密钥产生不同结果正常")
except Exception as e:
    print(f"❌ 不同密钥测试失败: {e}")

# 测试5：验证自定义密钥加密解密
print("\n[测试5] 验证自定义密钥加密解密")
try:
    key = "my_custom_password"
    e = Encryptor(key=key)
    data = "Sensitive information"
    encrypted = e.encrypt(data, key=key)
    decrypted = e.decrypt(encrypted, key=key)
    assert decrypted == data.encode("utf-8")
    print("✅ 自定义密钥加密解密正常")
except Exception as e:
    print(f"❌ 自定义密钥加密解密失败: {e}")

# 测试6：验证文件加密解密
print("\n[测试6] 验证文件加密解密")
try:
    e = Encryptor(key="file_key")
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as f:
        original = b"File content to encrypt and decrypt"
        f.write(original)
        src_path = f.name
    enc_path = e.encrypt_file(src_path, key="file_key")
    dec_path = e.decrypt_file(enc_path, key="file_key")
    with open(dec_path, "rb") as f:
        result = f.read()
    assert result == original
    os.remove(src_path)
    os.remove(enc_path)
    os.remove(dec_path)
    print("✅ 文件加密解密正常")
except Exception as e:
    print(f"❌ 文件加密解密测试失败: {e}")

# 测试7：验证空数据
print("\n[测试7] 验证空数据")
try:
    e = Encryptor(key="test")
    data = ""
    encrypted = e.encrypt(data)
    decrypted = e.decrypt(encrypted)
    assert decrypted == b""
    print("✅ 空数据加密解密正常")
except Exception as e:
    print(f"❌ 空数据测试失败: {e}")

# 测试8：验证长数据
print("\n[测试8] 验证长数据")
try:
    e = Encryptor(key="long_data_key")
    data = "A" * 10000
    encrypted = e.encrypt(data)
    decrypted = e.decrypt(encrypted)
    assert decrypted == data.encode("utf-8")
    print("✅ 长数据加密解密正常")
except Exception as e:
    print(f"❌ 长数据测试失败: {e}")

# 测试9：验证密钥派生
print("\n[测试9] 验证密钥派生")
try:
    e = Encryptor()
    key = e._derive_key("password", length=16)
    assert len(key) == 16
    key2 = e._derive_key("password", length=32)
    assert len(key2) == 32
    print("✅ 密钥派生正常")
except Exception as e:
    print(f"❌ 密钥派生测试失败: {e}")

# 测试10：验证错误密钥解密失败
print("\n[测试10] 验证错误密钥解密失败")
try:
    e1 = Encryptor(key="correct_key")
    data = b"secret"
    encrypted = e1.encrypt(data)
    e2 = Encryptor(key="wrong_key")
    decrypted = e2.decrypt(encrypted)
    assert decrypted != data
    print("✅ 错误密钥解密产生不同结果")
except Exception as e:
    print(f"❌ 错误密钥测试失败: {e}")

# 测试11：验证自动生成密钥
print("\n[测试11] 验证自动生成密钥")
try:
    e = Encryptor()
    assert len(e.key) == 32
    e2 = Encryptor()
    assert e.key != e2.key
    print("✅ 自动生成密钥正常")
except Exception as e:
    print(f"❌ 自动生成密钥测试失败: {e}")

# 测试12：验证中文加密
print("\n[测试12] 验证中文加密")
try:
    e = Encryptor(key="chinese_key")
    data = "中文测试数据，包含特殊字符！"
    encrypted = e.encrypt(data)
    decrypted = e.decrypt(encrypted)
    assert decrypted == data.encode("utf-8")
    print("✅ 中文加密正常")
except Exception as e:
    print(f"❌ 中文加密测试失败: {e}")

print("\n" + "=" * 60)
print("阶段35测试完成！")
print("=" * 60)
